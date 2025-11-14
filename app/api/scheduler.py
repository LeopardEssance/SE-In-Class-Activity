"""Scheduler endpoints."""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List
import uuid

from app.api.models import ScheduleTaskRequest, TaskResponse
from app.api.storage import dashboards_db, scheduler, notification_service
from app.api.auth import get_user_from_session
from app.models.scheduler import ScheduledTask

router = APIRouter(prefix="/schedule", tags=["Scheduler"])


@router.get("", response_model=List[TaskResponse])
async def get_scheduled_tasks(session_id: str = Query(..., description="Session ID")):
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


@router.post("", response_model=TaskResponse)
async def create_scheduled_task(request: ScheduleTaskRequest, session_id: str = Query(..., description="Session ID")):
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


@router.delete("/{task_id}")
async def cancel_scheduled_task(task_id: str, session_id: str = Query(..., description="Session ID")):
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

