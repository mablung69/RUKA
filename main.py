from controller import Controller
import variables as v

if __name__ == '__main__':
    print('----- PiTooth -----\n')
    controller = Controller(intensity_threshold=v.intensity_threshold,
                            connection_attempts=v.connection_attempts,
                            checker_delay=v.checker_delay)
