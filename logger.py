import threading
import time
import datetime
import os
from current_sensor import CurrentSensor


class Logger:
    def __init__(self, logging_delay, file_name, sensor_pin):
        self.logging_delay = logging_delay
        self.file_name = file_name

        self.current_sensor = CurrentSensor(sensor_pin=sensor_pin)

        self.check_file_exists()

        logger_thread = threading.Thread(name='Logger',
                                         target=self.continously_log,
                                         daemon=True)
        logger_thread.start()

    def check_file_exists(self):
        if not os.path.isfile(self.file_name):
            with open(self.file_name, 'w') as file:
                header = ['Año', 'Mes', 'Día', 'Hora', 'Minuto', 'Segundo',
                          'Amperaje [mA]']
                file.write(','.join(header) + '\n')

    def continously_log(self):
        while True:
            self.log()
            time.sleep(self.logging_delay)

    def log(self):
        with open(self.file_name, 'a') as file:
            data = map(str,
                       [datetime.datetime.now().year,
                        datetime.datetime.now().month,
                        datetime.datetime.now().day,
                        datetime.datetime.now().hour,
                        datetime.datetime.now().minute,
                        datetime.datetime.now().second,
                        self.current_sensor.miliamps])
            file.write(','.join(data) + '\n')
