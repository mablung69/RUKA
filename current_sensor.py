import Adafruit_ADS1x15
import math
import time


class CurrentSensor:
    def __init__(self, pin=0, gain=4, samples=200, decimal_places=2):
        self.adc = Adafruit_ADS1x15.ADS1015()
        self.pin = pin

        self.gain = gain
        self.samples = samples
        self.decimal_places = decimal_places

    def get_amps(self):
        count = 0
        max_value = 0

        while count < self.samples:
            max_value = max(abs(self.adc.read_adc(self.pin, gain=self.gain)),
                            max_value)
            count += 1

        i_rms = round(max_value / (2047 * 30), self.decimal_places)
        amps = round(i_rms / math.sqrt(2), self.decimal_places)

        return amps


if __name__ == '__main__':
    current_sensor = CurrentSensor()
    while True:
        print(current_sensor.get_amps())
        time.sleep(3)
