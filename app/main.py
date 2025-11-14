from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

from .models.user import User
from .models.device import Device, Light
from .models.dashboard import Dashboard
from .models.scheduler import Scheduler, ScheduledTask
from .models.device_factory import DeviceFactory
from .models.notification_service import NotificationService, Event

# Initialize FastAPI app
app = FastAPI(
    title="Smart Home IoT System",
    description="Backend API for Smart Home IoT System with device control and scheduling",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite and React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
users_db: Dict[str, User] = {}
dashboards_db: Dict[str, Dashboard] = {}
scheduler = Scheduler()
notification_service = NotificationService()
device_factory = DeviceFactory.get_instance()
current_sessions: Dict[str, str] = {}  # session_id -> user_id

# Initialize with a default user
default_user = User("user1", "admin", "password123")
users_db["admin"] = default_user
dashboards_db["user1"] = Dashboard("user1")

# Add some default devices
default_light1 = Light("light1", "Living Room Light")
default_light2 = Light("light2", "Bedroom Light")
dashboards_db["user1"].add_device(default_light1)
dashboards_db["user1"].add_device(default_light2)


# Pydantic Models
class LoginRequest(BaseModel):
    """Login request model."""
    username: str = Field(..., min_length=1, description="Username")
    password: str = Field(..., min_length=1, description="Password")


class LoginResponse(BaseModel):
    """Login response model."""
    success: bool
    message: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None


class LogoutResponse(BaseModel):
    """Logout response model."""
    success: bool
    message: str


class DeviceResponse(BaseModel):
    """Device response model."""
    device_id: str
    device_name: str
    device_type: str
    status: str
    brightness: Optional[int] = None
    is_on: Optional[bool] = None


class CreateDeviceRequest(BaseModel):
    """Create device request model."""
    device_type: str = Field(..., description="Type of device (light, thermostat, security_camera)")
    device_name: str = Field(..., min_length=1, description="Name of the device")


class BrightnessRequest(BaseModel):
    """Brightness control request model."""
    brightness: int = Field(..., ge=0, le=100, description="Brightness level (0-100)")


class ToggleResponse(BaseModel):
    """Toggle response model."""
    device_id: str
    is_on: bool
    status: str


class ScheduleTaskRequest(BaseModel):
    """Schedule task request model."""
    device_id: str = Field(..., description="ID of the device")
    action: str = Field(..., description="Action to perform (turn_on, turn_off, set_brightness)")
    scheduled_time: str = Field(..., description="ISO format datetime string")
    brightness: Optional[int] = Field(None, ge=0, le=100, description="Brightness level for lights")


class TaskResponse(BaseModel):
    """Task response model."""
    task_id: str
    device_id: str
    action: str
    scheduled_time: str
    executed: bool


class NotificationResponse(BaseModel):
    """Notification response model."""
    event_type: str
    device_id: str
    message: str
    data: Dict[str, Any]
    timestamp: str


# Helper functions
def get_user_from_session(session_id: str) -> Optional[User]:
    """Get user from session ID."""
    user_id = current_sessions.get(session_id)
    if user_id:
        for user in users_db.values():
            if user.user_id == user_id:
                return user
    return None


# Authentication Endpoints
@app.post("/auth/login", response_model=LoginResponse, tags=["Authentication"])
async def login(request: LoginRequest):
    """
    Authenticate user and create session.

    Default credentials: username='admin', password='password123'
    """
    try:
        # Find user by username
        user = users_db.get(request.username)

        if not user:
            return LoginResponse(
                success=False,
                message="Invalid username or password"
            )

        # Verify credentials
        if user.login(request.username, request.password):
            session_id = str(uuid.uuid4())
            current_sessions[session_id] = user.user_id

            return LoginResponse(
                success=True,
                message="Login successful",
                user_id=user.user_id,
                session_id=session_id
            )
        else:
            return LoginResponse(
                success=False,
                message="Invalid username or password"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@app.post("/auth/logout", response_model=LogoutResponse, tags=["Authentication"])
async def logout(session_id: str):
    """Logout user and destroy session."""
    try:
        user = get_user_from_session(session_id)

        if not user:
            return LogoutResponse(
                success=False,
                message="Invalid session"
            )

        user.logout()
        current_sessions.pop(session_id, None)

        return LogoutResponse(
            success=True,
            message="Logout successful"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout failed: {str(e)}"
        )


# Device Endpoints
@app.get("/devices", response_model=List[DeviceResponse], tags=["Devices"])
async def get_devices(session_id: str):
    """Get all devices for the logged-in user."""
    try:
        user = get_user_from_session(session_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session. Please login."
            )

        dashboard = dashboards_db.get(user.user_id)

        if not dashboard:
            return []

        devices_data = dashboard.display_devices()
        return devices_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve devices: {str(e)}"
        )


@app.post("/devices", response_model=DeviceResponse, tags=["Devices"])
async def create_device(request: CreateDeviceRequest, session_id: str):
    """Create a new device and add to user's dashboard."""
    try:
        user = get_user_from_session(session_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session. Please login."
            )

        # Create device using factory
        config = {
            "device_id": str(uuid.uuid4()),
            "device_name": request.device_name
        }

        device = device_factory.create_device(request.device_type, config)

        # Add to user's dashboard
        dashboard = dashboards_db.get(user.user_id)

        if not dashboard:
            dashboard = Dashboard(user.user_id)
            dashboards_db[user.user_id] = dashboard

        if dashboard.add_device(device):
            # Send notification
            notification_service.send_notification(
                f"New device '{device.device_name}' added",
                device.device_id,
                "device_added"
            )

            return device.to_dict()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Device already exists"
            )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create device: {str(e)}"
        )


@app.put("/devices/{device_id}/light/brightness", response_model=DeviceResponse, tags=["Devices"])
async def set_light_brightness(device_id: str, request: BrightnessRequest, session_id: str):
    """Set brightness for a light device."""
    try:
        user = get_user_from_session(session_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session. Please login."
            )

        dashboard = dashboards_db.get(user.user_id)

        if not dashboard:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dashboard not found"
            )

        device = dashboard.get_device(device_id)

        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found"
            )

        if not isinstance(device, Light):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Device is not a light"
            )

        if device.set_brightness(request.brightness):
            # Send notification
            notification_service.send_notification(
                f"Light '{device.device_name}' brightness set to {request.brightness}%",
                device.device_id,
                "brightness_changed"
            )

            return device.to_dict()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid brightness level"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to set brightness: {str(e)}"
        )


@app.post("/devices/{device_id}/toggle", response_model=ToggleResponse, tags=["Devices"])
async def toggle_device(device_id: str, session_id: str):
    """Toggle a light device on/off."""
    try:
        user = get_user_from_session(session_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session. Please login."
            )

        dashboard = dashboards_db.get(user.user_id)

        if not dashboard:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dashboard not found"
            )

        device = dashboard.get_device(device_id)

        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found"
            )

        if not isinstance(device, Light):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Device is not a light"
            )

        is_on = device.toggle()

        # Send notification
        notification_service.send_notification(
            f"Light '{device.device_name}' toggled {'on' if is_on else 'off'}",
            device.device_id,
            "device_toggled"
        )

        return ToggleResponse(
            device_id=device.device_id,
            is_on=is_on,
            status=device.status
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to toggle device: {str(e)}"
        )


@app.delete("/devices/{device_id}", tags=["Devices"])
async def delete_device(device_id: str, session_id: str):
    """Delete a device from user's dashboard."""
    try:
        user = get_user_from_session(session_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session. Please login."
            )

        dashboard = dashboards_db.get(user.user_id)

        if not dashboard:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dashboard not found"
            )

        if dashboard.remove_device(device_id):
            return {"success": True, "message": "Device removed successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete device: {str(e)}"
        )


# Scheduler Endpoints
@app.get("/schedule", response_model=List[TaskResponse], tags=["Scheduler"])
async def get_scheduled_tasks(session_id: str):
    """Get all scheduled tasks."""
    try:
        user = get_user_from_session(session_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session. Please login."
            )

        tasks = scheduler.get_scheduled_tasks()
        return tasks
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve scheduled tasks: {str(e)}"
        )


@app.post("/schedule", response_model=TaskResponse, tags=["Scheduler"])
async def create_scheduled_task(request: ScheduleTaskRequest, session_id: str):
    """Create a new scheduled task."""
    try:
        user = get_user_from_session(session_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session. Please login."
            )

        # Verify device exists
        dashboard = dashboards_db.get(user.user_id)

        if not dashboard:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dashboard not found"
            )

        device = dashboard.get_device(request.device_id)

        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found"
            )

        # Create task
        task_id = str(uuid.uuid4())
        task = ScheduledTask(
            task_id=task_id,
            device_id=request.device_id,
            action=request.action,
            scheduled_time=request.scheduled_time
        )

        scheduler.schedule_task(task)

        # Send notification
        notification_service.send_notification(
            f"Task scheduled for device '{device.device_name}' at {request.scheduled_time}",
            device.device_id,
            "task_scheduled"
        )

        return task.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create scheduled task: {str(e)}"
        )


@app.delete("/schedule/{task_id}", tags=["Scheduler"])
async def cancel_scheduled_task(task_id: str, session_id: str):
    """Cancel a scheduled task."""
    try:
        user = get_user_from_session(session_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session. Please login."
            )

        if scheduler.cancel_task(task_id):
            return {"success": True, "message": "Task cancelled successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel task: {str(e)}"
        )


# Notification Endpoints
@app.get("/notifications", response_model=List[NotificationResponse], tags=["Notifications"])
async def get_notifications(session_id: str, limit: int = 10):
    """Get recent notifications."""
    try:
        user = get_user_from_session(session_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session. Please login."
            )

        notifications = notification_service.get_notifications(limit)
        return notifications
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve notifications: {str(e)}"
        )


# Health check endpoint
@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "status": "running",
        "message": "Smart Home IoT System API",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
