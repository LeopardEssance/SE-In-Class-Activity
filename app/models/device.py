class device:
  deviceId: str
  deviceName: str
  status: str
  deviceType: str


  def __init__(self, deviceId, deviceName, deviceType):
    self.deviceId = deviceId
    self.deviceName = deviceName
    self.deviceType = deviceType
    self.status = "created"

  def turnOn(self):
    self.status = "on"

  def turnOff(self):
    self.status = "off"

  def getStatus(self):
    return self.status

  def configure(self):
    pass
    # Implemented Later
