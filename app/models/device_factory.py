class DeviceFactory:

    @staticmethod
    def getInstance():
        
        if DeviceFactory._instance is None:
            DeviceFactory._instance = DeviceFactory()
        return DeviceFactory._instance

    def createDevice(self, device_type):
        # Import here to avoid circular dependencies
        from app.models.thermostat import Thermostat
        from app.models.security_camera import SecurityCamera

        device_type = device_type.lower()

        if device_type == 'thermostat':
            return Thermostat()
        elif device_type == 'securitycamera' or device_type == 'security_camera':
            return SecurityCamera()
        else:
            raise ValueError(f"Unknown device type: {device_type}")

    def configureDevice(self, device):
        # Turn on the device by default
        device.turnOn()

        # Additional configuration can be added here
        print(f"Device {device.deviceName} has been configured and is ready to use.")