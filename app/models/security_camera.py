from app.models.device import Device


class SecurityCamera(Device):
    
    def __init__(self, device_id=None, device_name="Security Camera", resolution="1080p"):
        
        super().__init__(device_id, device_name, device_type="SecurityCamera")
        self.isRecording = False
        self.resolution = resolution

    def startRecording(self):
        
        if self.status != "on":
            print(f"Cannot start recording: {self.deviceName} is turned off.")
            return

        if self.isRecording:
            print(f"{self.deviceName} is already recording.")
            return

        self.isRecording = True
        print(f"{self.deviceName} has started recording at {self.resolution}.")

    def stopRecording(self):
        
        if not self.isRecording:
            print(f"{self.deviceName} is not currently recording.")
            return

        self.isRecording = False
        print(f"{self.deviceName} has stopped recording.")

    def captureImage(self):
        
        if self.status != "on":
            print(f"Cannot capture image: {self.deviceName} is turned off.")
            return None

        image_filename = f"{self.deviceId}_capture.jpg"
        print(f"{self.deviceName} captured an image: {image_filename}")
        return image_filename

    def getStatus(self):
        
        base_status = super().getStatus()
        recording_status = "recording" if self.isRecording else "not recording"
        return f"{base_status}, {recording_status}, resolution: {self.resolution}"