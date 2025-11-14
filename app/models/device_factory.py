from typing import Optional, Dict, Any
from models.device import Device, Light
import uuid


class Thermostat(Device):
    """Thermostat device for temperature control."""

    def __init__(self, device_id: str, device_name: str):
        """Initialize a thermostat device."""
        super().__init__(device_id, device_name, "thermostat")
        self.temperature: float = 20.0
        self.target_temperature: float = 22.0

    def set_temperature(self, temp: float) -> bool:
        """Set target temperature."""
        if 10.0 <= temp <= 35.0:
            self.target_temperature = temp
            return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        """Convert thermostat to dictionary."""
        base_dict = super().to_dict()
        base_dict.update({
            "temperature": self.temperature,
            "target_temperature": self.target_temperature
        })
        return base_dict


class SecurityCamera(Device):
    """Security camera device."""

    def __init__(self, device_id: str, device_name: str):
        """Initialize a security camera device."""
        super().__init__(device_id, device_name, "security_camera")
        self.recording: bool = False

    def start_recording(self) -> None:
        """Start recording."""
        self.recording = True
        self.status = "recording"

    def stop_recording(self) -> None:
        """Stop recording."""
        self.recording = False
        self.status = "on"

    def to_dict(self) -> Dict[str, Any]:
        """Convert camera to dictionary."""
        base_dict = super().to_dict()
        base_dict.update({
            "recording": self.recording
        })
        return base_dict


class DeviceFactory:
    """Singleton factory for creating devices."""

    _instance: Optional['DeviceFactory'] = None

    def __new__(cls):
        """Ensure only one instance exists (Singleton pattern)."""
        if cls._instance is None:
            cls._instance = super(DeviceFactory, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def get_instance() -> 'DeviceFactory':
        """
        Get the singleton instance of DeviceFactory.

        Returns:
            DeviceFactory: The singleton instance
        """
        if DeviceFactory._instance is None:
            DeviceFactory._instance = DeviceFactory()
        return DeviceFactory._instance

    def create_device(self, device_type: str, config: Optional[Dict[str, Any]] = None) -> Device:
        """
        Create a device of the specified type.

        Args:
            device_type: Type of device ('light', 'thermostat', 'security_camera')
            config: Configuration dictionary with device_id and device_name

        Returns:
            Device: Created device instance

        Raises:
            ValueError: If device type is unknown
        """
        device_type = device_type.lower()

        # Use config or generate defaults
        device_id = config.get("device_id", str(uuid.uuid4())) if config else str(uuid.uuid4())
        device_name = config.get("device_name", f"{device_type}_{device_id[:8]}") if config else f"{device_type}_{device_id[:8]}"

        if device_type == 'light':
            device = Light(device_id, device_name)
        elif device_type == 'thermostat':
            device = Thermostat(device_id, device_name)
        elif device_type in ['securitycamera', 'security_camera']:
            device = SecurityCamera(device_id, device_name)
        else:
            raise ValueError(f"Unknown device type: {device_type}")

        return device

    def configure_device(self, device: Device, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Configure a device with custom settings.

        Args:
            device: Device to configure
            config: Configuration dictionary
        """
        if config:
            device.configure(config)
        else:
            # Default configuration: turn on the device
            device.turn_on()