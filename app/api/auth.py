"""Authentication endpoints."""
from fastapi import APIRouter, HTTPException, status, Query
import uuid
from typing import Optional

from app.api.models import LoginRequest, LoginResponse, LogoutResponse
from app.api.storage import users_db, current_sessions
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_user_from_session(session_id: str) -> Optional[User]:
    """Get user from session ID."""
    user_id = current_sessions.get(session_id)
    if user_id:
        for user in users_db.values():
            if user.user_id == user_id:
                return user
    return None


@router.post("/login", response_model=LoginResponse)
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


@router.post("/logout", response_model=LogoutResponse)
async def logout(session_id: str = Query(..., description="Session ID")):
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

