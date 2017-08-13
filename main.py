from gpio_controller import GPIOController
import bluetooth_controller
import threading

gpio = GPIOController()


def discover_nearby_devices():
    while True:
        gpio.block_until_press()
        print('Looking for devices...')
        nearby_devices = bluetooth_controller.get_nearby_devices()
        print('Found these devices: {}'.format(nearby_devices))

if __name__ == '__main__':
    discoverer_thread = threading.Thread(name='Discoverer',
                                         target=discover_nearby_devices)
    discoverer_thread.start()
