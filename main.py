from controller import Controller
from logger import Logger
import bluetooth_variables as b_v
import logger_variables as l_v

if __name__ == '__main__':
    print('----- PiTooth -----\n')
    logger = Logger(l_v.logging_delay, l_v.file_name, l_v.pin)
    controller = Controller(intensity_threshold=b_v.intensity_threshold,
                            connection_attempts=b_v.connection_attempts,
                            checker_delay=b_v.checker_delay)
