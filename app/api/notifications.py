"""Notifications endpoints."""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Dict, Any

from app.api.storage import notification_service
from app.api.auth import get_user_from_session

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=List[Dict[str, Any]])
async def get_notifications(
    session_id: str = Query(..., description="Session ID"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of notifications to return")
):
    """Get recent notifications for the logged-in user."""
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

