import datetime
import uuid


class UserPublic:
    def __init__(self, id: uuid.UUID, is_verified: bool, username: str, password: str, created_at: datetime.datetime):
        self.id = id
        self.is_verified = is_verified
        self.username = username
        self.password = password
        self.created_at = created_at
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

    def logout(self) -> bool:
        """
        Log out the current user.
        
        Returns:
            bool: True if logout successful, False if not logged in
        """
        if self._is_logged_in:
            self._is_logged_in = False
            return True
        return False