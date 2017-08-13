from gpio_controller import GPIOController
import bluetooth_controller
import threading
import time


class Controller:
    def __init__(self, threshold):
        GPIOController()

        self.threshold = threshold
        self.closest_device = None

        discoverer_thread = threading.Thread(name='Discoverer',
                                             target=self.seek_closest_device)
        intensity_checker_thread = threading.Thread(
            name='Intensity checker',
            target=self.check_closest_device_intensity)
        discoverer_thread.start()
        intensity_checker_thread.start()

    def seek_closest_device(self):
        while True:
            GPIOController.block_until_press()
            print('Looking for devices...')
            nearby_devices = bluetooth_controller.get_nearby_devices(True)

            if nearby_devices:
                print('Found these devices: {}'.format(nearby_devices))
                intensities = []
                for device in nearby_devices:
                    intensity = None
                    attempts = 0
                    while intensity is None and attempts < 3:
                        intensity = bluetooth_controller.get_rssi(device[0])
                        attempts += 1
                    intensities.append(intensity)
                print('Intensities: {}'.format(intensities))
                if list(filter(lambda x: x is not None, intensities)):
                    self.closest_device = nearby_devices[intensities.index(max(
                        list(filter(lambda x: x is not None, intensities))))]
                    print('The closest device is: {}'.format(
                        self.closest_device))
                else:
                    print('The devices were not found.')
            else:
                print('Found no devices nearby.')

    def check_closest_device_intensity(self):
        while True:
            if self.closest_device:
                intensity = None
                attempts = 0
                while intensity is None and attempts < 2:
                    intensity = bluetooth_controller.get_rssi(
                        self.closest_device[0])
                    print('Intensity: {}'.format(intensity))
                    if intensity is None:
                        attempts += 1
                        print('Device not found. Retrying...')
                if intensity is None:
                    GPIOController.set_led(False)
                    print('Device not found. Turning LED off.')
                elif intensity < self.threshold:
                    GPIOController.set_led(False)
                    print('Below threshold.')
                else:
                    GPIOController.set_led(True)
                    print('Above threshold.')
                time.sleep(5)
            else:
                time.sleep(1)
