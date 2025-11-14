from typing import Dict, Optional
import hashlib


class User:
    """User class for authentication and session management."""

    def __init__(self, user_id: str, username: str, password: str):
        """
        Initialize a user.

        Args:
            user_id: Unique identifier for the user
            username: Username for login
            password: Password (stored as-is for simplicity, in production use hashing)
        """
        self.user_id = user_id
        self.username = username
        self.password = password
        self._is_logged_in = False

    def login(self, username: str, password: str) -> bool:
        """
        Authenticate user with username and password.

        Args:
            username: The username to authenticate
            password: The password to authenticate

        Returns:
            bool: True if login successful, False otherwise
        """
        if self.username == username and self.password == password:
            self._is_logged_in = True
            return True
        return False

    def logout(self) -> None:
        """Log out the current user."""
        self._is_logged_in = False

    def is_logged_in(self) -> bool:
        """
        Check if user is currently logged in.

        Returns:
            bool: True if logged in, False otherwise
        """
        return self._is_logged_in

    def to_dict(self) -> Dict[str, str]:
        """
        Convert user to dictionary representation (without password).

        Returns:
            Dict containing safe user data
        """
        return {
            "user_id": self.user_id,
            "username": self.username,
            "is_logged_in": self._is_logged_in
        }