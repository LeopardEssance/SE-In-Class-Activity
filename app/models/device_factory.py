from typing import Optional, Dict, Any, Type, Callable
from app.models.device import Device, Light, Thermostat, SecurityCamera
import uuid


# Thermostat and Light are implemented in their own modules (app/models/thermostat.py and
# app/models/light.py) to keep device implementations separate and importable by the frontend
# and factory.


# SecurityCamera is implemented in app/models/security_camera.py to avoid duplicate
# class definitions and to keep device-specific classes in their own module.


class DeviceFactory:
    """Singleton factory for creating devices."""

    _instance: Optional['DeviceFactory'] = None
    
    # Registry mapping device types to their constructor functions
    _device_registry: Dict[str, Callable[[str, str], Device]] = {
        'light': Light,
        'thermostat': Thermostat,
        'security_camera': SecurityCamera,
        'securitycamera': SecurityCamera,  # Support alternative naming
    }

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

    @classmethod
    def register_device(cls, device_type: str, device_class: Type[Device]) -> None:
        """
        Register a new device type in the factory registry.
        
        Args:
            device_type: String identifier for the device type
            device_class: Device class to instantiate
        """
        cls._device_registry[device_type.lower()] = device_class

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

        # Look up device class in registry
        device_class = self._device_registry.get(device_type)
        if device_class is None:
            raise ValueError(f"Unknown device type: {device_type}")
        
        device = device_class(device_id, device_name)
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