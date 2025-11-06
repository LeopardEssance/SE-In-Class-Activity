class Thermostat:
    def __init__(self):
        self.temperature = 0
        self.mode = "off"

    def setTemperature(self, temperature: int):
        self.temperature = temperature

    def getTemperature(self) -> int:
        return self.temperature

    def setMode(self, mode: str):
        self.mode = mode
