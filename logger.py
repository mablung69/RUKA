# -*- coding: utf-8 -*-
import threading
import time
import datetime
import os
from random import randint
from current_sensor import CurrentSensor

from eventModule import getBroadcaster
broadcasterSingleton = getBroadcaster()

class Logger:
    def __init__(self, logging_delay, file_name, sensor_pin, state):
        self.state = state
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
        if not self.state=="develop":
            amps = self.current_sensor.miliamps
        else:
            amps = randint(0,100)
        data = map(str,
                   [datetime.datetime.now().year,
                    datetime.datetime.now().month,
                    datetime.datetime.now().day,
                    datetime.datetime.now().hour,
                    datetime.datetime.now().minute,
                    datetime.datetime.now().second,
                    amps])
        if not self.state=="develop":
            with open(self.file_name, 'a') as file:                
                file.write(','.join(data) + '\n')
        #llamar al modulo que guarda los datos
        broadcasterSingleton.event["log_data"].call(','.join(data))
