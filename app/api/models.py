"""Pydantic models for API requests and responses."""
from pydantic import BaseModel, Field
from typing import Optional, List


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

