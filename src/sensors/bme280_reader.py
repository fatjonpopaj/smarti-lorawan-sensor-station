"""BME280 temperature and humidity reader using I2C."""
import bme280
import smbus2

class BME280Reader:
    def __init__(self, bus_number=1, address=0x76):
        self.bus = smbus2.SMBus(bus_number)
        self.address = address
        self.calibration = bme280.load_calibration_params(self.bus, self.address)

    def read(self):
        sample = bme280.sample(self.bus, self.address, self.calibration)
        return float(sample.temperature), float(sample.humidity)

    def close(self):
        self.bus.close()
