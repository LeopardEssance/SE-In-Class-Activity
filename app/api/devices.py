"""Device management endpoints."""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List
import uuid

from app.api.models import (
    DeviceResponse,
    CreateDeviceRequest,
    BrightnessRequest,
    ToggleResponse
)
from app.api.storage import (
    dashboards_db,
    device_factory,
    notification_service
)
from app.api.auth import get_user_from_session
from app.models.device import Light
from app.models.dashboard import Dashboard

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get("", response_model=List[DeviceResponse])
async def get_devices(session_id: str = Query(..., description="Session ID")):
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


@router.post("", response_model=DeviceResponse)
async def create_device(request: CreateDeviceRequest, session_id: str = Query(..., description="Session ID")):
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


@router.put("/{device_id}/light/brightness", response_model=DeviceResponse)
async def set_light_brightness(device_id: str, request: BrightnessRequest, session_id: str = Query(..., description="Session ID")):
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


@router.post("/{device_id}/toggle", response_model=ToggleResponse)
async def toggle_device(device_id: str, session_id: str = Query(..., description="Session ID")):
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


@router.delete("/{device_id}")
async def delete_device(device_id: str, session_id: str = Query(..., description="Session ID")):
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

