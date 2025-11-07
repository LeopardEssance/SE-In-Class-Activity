import app.models.device as device;

class dashboard:
  deviceList: list[device.Device] #List of devices
  userId: str

  def __init__(self, userId):
    self.userId = userId
    self.deviceList = []

  def displayDevices(self):
    #to be implemented later
    pass

  def refreshStatus(self):
    #to be implemented later
    pass

  def addDevice(self, device: device.device):
    #to be implemented later
    pass

  def removeDevice(self, deviceId: str):
    #to be implemented later
    pass