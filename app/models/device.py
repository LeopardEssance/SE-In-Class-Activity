from typing import Optional, Dict, Any
from abc import ABC, abstractmethod


class Device(ABC):
    """Base class for all smart home devices."""

    def __init__(self, device_id: str, device_name: str, device_type: str):
        """
        Initialize a device.

        Args:
            device_id: Unique identifier for the device
            device_name: Human-readable name for the device
            device_type: Type of device (e.g., 'light', 'thermostat', 'camera')
        """
        self.device_id = device_id
        self.device_name = device_name
        self.device_type = device_type
        self.status = "off"

    def turn_on(self) -> None:
        """Turn the device on."""
        self.status = "on"

    def turn_off(self) -> None:
        """Turn the device off."""
        self.status = "off"

    def get_status(self) -> str:
        """
        Get the current status of the device.

        Returns:
            str: Current status ('on' or 'off')
        """
        return self.status

    def configure(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Configure the device with custom settings.

        Args:
            config: Dictionary of configuration parameters
        """
        if config:
            for key, value in config.items():
                if hasattr(self, key):
                    setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert device to dictionary representation.

        Returns:
            Dict containing device data
        """
        return {
            "device_id": self.device_id,
            "device_name": self.device_name,
            "device_type": self.device_type,
            "status": self.status
        }


class Light(Device):
    """Light device with brightness control."""

    def __init__(self, device_id: str, device_name: str):
        """
        Initialize a light device.

        Args:
            device_id: Unique identifier for the light
            device_name: Human-readable name for the light
        """
        super().__init__(device_id, device_name, "light")
        self.brightness: int = 0
        self.is_on: bool = False

    def turn_on(self) -> None:
        """Turn the light on and set default brightness."""
        super().turn_on()
        self.is_on = True
        if self.brightness == 0:
            self.brightness = 100

    def turn_off(self) -> None:
        """Turn the light off."""
        super().turn_off()
        self.is_on = False
        self.brightness = 0

    def set_brightness(self, level: int) -> bool:
        """
        Set the brightness level of the light.

        Args:
            level: Brightness level (0-100)

        Returns:
            bool: True if successful, False if invalid level
        """
        if 0 <= level <= 100:
            self.brightness = level
            if level > 0:
                self.is_on = True
                self.status = "on"
            else:
                self.is_on = False
                self.status = "off"
            return True
        return False

    def get_brightness(self) -> int:
        """
        Get the current brightness level.

        Returns:
            int: Current brightness (0-100)
        """
        return self.brightness

    def toggle(self) -> bool:
        """
        Toggle the light on/off state.

        Returns:
            bool: New state (True=on, False=off)
        """
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()
        return self.is_on

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert light to dictionary representation.

        Returns:
            Dict containing light data including brightness
        """
        base_dict = super().to_dict()
        base_dict.update({
            "brightness": self.brightness,
            "is_on": self.is_on
        })
        return base_dict
