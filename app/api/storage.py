"""In-memory storage and initialization for the API."""
from typing import Dict
from app.models.user import User
from app.models.device import Light
from app.models.dashboard import Dashboard
from app.models.scheduler import Scheduler
from app.models.device_factory import DeviceFactory
from app.models.notification_service import NotificationService

# In-memory storage
users_db: Dict[str, User] = {}
dashboards_db: Dict[str, Dashboard] = {}
scheduler = Scheduler()
notification_service = NotificationService()
device_factory = DeviceFactory.get_instance()
current_sessions: Dict[str, str] = {}  # session_id -> user_id


def initialize_default_data():
    """Initialize with default user and devices."""
    default_user = User("user1", "admin", "password123")
    users_db["admin"] = default_user
    dashboards_db["user1"] = Dashboard("user1")

    # Add some default devices
    default_light1 = Light("light1", "Living Room Light")
    default_light2 = Light("light2", "Bedroom Light")
    dashboards_db["user1"].add_device(default_light1)
    dashboards_db["user1"].add_device(default_light2)


# Initialize on import
initialize_default_data()

