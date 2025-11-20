from typing import List, Optional, Dict, Any
from app.models.device import Device


class Dashboard:
    """Central controller for managing user devices."""

    def __init__(self, user_id: str):
        """
        Initialize a dashboard for a user.

        Args:
            user_id: User identifier this dashboard belongs to
        """
        self.user_id = user_id
        self.devices: Dict[str, Device] = {}

    def display_devices(self) -> List[Dict[str, Any]]:
        """
        Display all devices with their current status.

        Returns:
            List of device dictionaries
        """
        return [device.to_dict() for device in self.devices.values()]

    def refresh_status(self) -> List[Dict[str, Any]]:
        """
        Refresh and return the status of all devices.

        Returns:
            List of device dictionaries with updated status
        """
        return self.display_devices()

    def add_device(self, device: Device) -> bool:
        """
        Add a device to the dashboard.

        Args:
            device: Device instance to add

        Returns:
            bool: True if added successfully, False if device already exists
        """
        # Check if device already exists
        if device.device_id in self.devices:
            return False

        self.devices[device.device_id] = device
        return True

    def remove_device(self, device_id: str) -> bool:
        """
        Remove a device from the dashboard.

        Args:
            device_id: ID of the device to remove

        Returns:
            bool: True if removed successfully, False if device not found
        """
        if device_id in self.devices:
            del self.devices[device_id]
            return True
        return False

    def get_device(self, device_id: str) -> Optional[Device]:
        """
        Get a device by its ID.

        Args:
            device_id: ID of the device to retrieve

        Returns:
            Device instance if found, None otherwise
        """
        return self.devices.get(device_id)

    def get_device_count(self) -> int:
        """
        Get the total number of devices.

        Returns:
            int: Number of devices in the dashboard
        """
        return len(self.devices)