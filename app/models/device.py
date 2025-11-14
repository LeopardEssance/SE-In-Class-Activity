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


# Device child classes
class Light(Device):
    """Light device with brightness control."""

    def __init__(self, device_id: str, device_name: str):
        super().__init__(device_id, device_name, "light")
        self.brightness: int = 0
        self.is_on: bool = False

    def turn_on(self) -> None:
        super().turn_on()
        self.is_on = True
        if self.brightness == 0:
            self.brightness = 100

    def turn_off(self) -> None:
        super().turn_off()
        self.is_on = False
        self.brightness = 0

    def set_brightness(self, level: int) -> bool:
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
        return self.brightness

    def toggle(self) -> bool:
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()
        return self.is_on

    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update({
            "brightness": self.brightness,
            "is_on": self.is_on
        })
        return base_dict


class Thermostat(Device):
    """Thermostat device for temperature control."""

    def __init__(self, device_id: str, device_name: str):
        super().__init__(device_id, device_name, "thermostat")
        self.temperature: float = 20.0
        self.target_temperature: float = 22.0

    def set_temperature(self, temp: float) -> bool:
        if 10.0 <= temp <= 35.0:
            self.target_temperature = temp
            return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update({
            "temperature": self.temperature,
            "target_temperature": self.target_temperature
        })
        return base_dict


class SecurityCamera(Device):
    """Security camera device."""

    def __init__(self, device_id: str, device_name: str = "Security Camera", resolution: str = "1080p"):
        super().__init__(device_id, device_name, device_type="security_camera")
        self.recording: bool = False
        self.resolution: str = resolution

    def start_recording(self) -> None:
        if self.status != "on":
            return
        if self.recording:
            return
        self.recording = True
        self.status = "recording"

    def stop_recording(self) -> None:
        if not self.recording:
            return
        self.recording = False
        self.status = "on"

    def capture_image(self) -> Optional[str]:
        if self.status != "on" and self.status != "recording":
            return None
        image_filename = f"{self.device_id}_capture.jpg"
        return image_filename

    def get_status(self) -> str:
        base_status = super().get_status()
        recording_status = "recording" if self.recording else "not recording"
        return f"{base_status}, {recording_status}, resolution: {self.resolution}"

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            "recording": self.recording,
            "resolution": self.resolution
        })
        return base
