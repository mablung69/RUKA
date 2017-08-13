from gpio_controller import GPIOController
import bluetooth_controller
import threading
import sys


class Controller:
    def __init__(self):
        GPIOController()
        
        self.closest_device = None

        discoverer_thread = threading.Thread(name='Discoverer',
                                             target=self.seek_closest_device)
        discoverer_thread.start()

    def seek_closest_device(self):
        while True:
            GPIOController.block_until_press()
            print('Looking for devices...')
            nearby_devices = bluetooth_controller.get_nearby_devices(True)

            if nearby_devices:
                print('Found these devices: {}'.format(nearby_devices))
                distances = []
                for device in nearby_devices:
                    distances.append(bluetooth_controller.get_rssi(device[0]))
                print('Distances: {}'.format(distances))

                self.closest_device = nearby_devices[nearby_devices.index(
                    max(distances))]
                print('The closest device is: {}'.format(self.closest_device))
            else:
                print('Found no devices nearby.')

if __name__ == '__main__':
    try:
        controller = Controller()
    except KeyboardInterrupt:
        GPIOController.cleanup()
        sys.exit()
