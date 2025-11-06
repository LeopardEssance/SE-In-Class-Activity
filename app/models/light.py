class Light:
    def __init__(self):
        self.brightness = 0
        self.isOn = False

    def setBrightness(self, brightness: int):
        self.brightness = brightness

    def getBrightness(self) -> int:
        return self.brightness

    def toggle(self):
        self.isOn = not self.isOn
