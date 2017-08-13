import bluetooth
import execnet


def get_nearby_devices(names=False):
    return bluetooth.discover_devices(lookup_names=names)


def get_rssi(address):
    version = '2.7'
    module_ = 'bluetooth_proximity.bt_rssi'
    function_ = 'get_rssi'

    gateway = execnet.makegateway('popen//python=python{}'.format(version))
    channel = gateway.remote_exec('''
        from {} import {} as the_function
        channel.send(the_function(*channel.receive()))
    '''.format(module_, function_))
    channel.send([address])
    return channel.receive()


if __name__ == '__main__':
    address = '7C:01:91:4D:FA:16'
    print(get_rssi(address))
