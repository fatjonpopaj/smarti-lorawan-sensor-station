"""Digital line tracker on Raspberry Pi GPIO17."""
from gpiozero import DigitalInputDevice

class LineTracker:
    def __init__(self, gpio_pin=17):
        self.device = DigitalInputDevice(gpio_pin)

    def read(self):
        return int(self.device.value)

    def close(self):
        self.device.close()
