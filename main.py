from controller import Controller
import variables as v

if __name__ == '__main__':
    print('----- PiTooth -----\n')
    controller = Controller(threshold=v.threshold,
                            attempts=v.attempts,
                            checker_delay=v.checker_delay)
