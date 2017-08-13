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
                    intensity = bluetooth_controller.get_rssi(device[0])
                    intensities.append(intensity)
                print('Intensities: {}'.format(intensities))

                self.closest_device = nearby_devices[intensities.index(max(
                    filter(lambda x: bool(x), intensities)))]
                print('The closest device is: {}'.format(self.closest_device))
            else:
                print('Found no devices nearby.')

    def check_closest_device_intensity(self):
        while True:
            if self.closest_device:
                intensity = bluetooth_controller.get_rssi(
                    self.closest_device[0])
                if not intensity:
                    GPIOController.set_led(False)
                    print('Device not found.')
                    time.sleep(5)
                elif intensity < self.threshold:
                    GPIOController.set_led(False)
                    print('Below threshold.')
                else:
                    GPIOController.set_led(True)
                    print('Above threshold.')
            else:
                print('There is no device stored.')
                time.sleep(5)
