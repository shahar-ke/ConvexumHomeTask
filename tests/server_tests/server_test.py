import logging
import os
from unittest import TestCase

from drone_data_lib.drone_position import DronePosition
from sensor_lib.com_utils.http_com_util import HTTPComUtil
from sensor_lib.drivers.sensor_driver_simulator import SensorDriverSimulator
from sensor_lib.sensor import Sensor

logging.basicConfig(level=logging.INFO)


class ServerTest(TestCase):
    GROUND_GROUND_STATES = [DronePosition.GROUND.value, DronePosition.GROUND.value]
    AIR_GROUND_STATES = [DronePosition.AIR.value, DronePosition.GROUND.value]

    def test_server(self):
        demo_drones_file_path = '../../task_def/drones.txt'
        abs_drones_file_path = os.path.abspath(demo_drones_file_path)
        sensor_driver = SensorDriverSimulator(input_file_path=abs_drones_file_path, sleep_time_sec=0.1)
        com_util = HTTPComUtil()
        sensor = Sensor(sensor_driver=sensor_driver, com_util=com_util)
        real_history = sensor.sense()
        drones_history = real_history['drones']
        drones_history = [drone_history[1:] for drone_history in drones_history]
        expected_res = [
            ['Phantom3'] + self.GROUND_GROUND_STATES,
            ['Mavic2'] + self.AIR_GROUND_STATES,
            ['blabla'] + self.GROUND_GROUND_STATES,
            ['superdrone'] + self.AIR_GROUND_STATES,
            ['Phantom3'] + self.AIR_GROUND_STATES,
            ['Mydrone'] + self.GROUND_GROUND_STATES,
            ['parrot'] + self.AIR_GROUND_STATES,
            ['newdrone'] + self.AIR_GROUND_STATES,
            ['droney'] + self.GROUND_GROUND_STATES,
            ['flyaway'] + self.GROUND_GROUND_STATES,
            ['newdrone'] + self.AIR_GROUND_STATES,
            ['airdrone'] + self.GROUND_GROUND_STATES,
            ['grounddrone'] + self.AIR_GROUND_STATES,
            ['d70#%'] + self.AIR_GROUND_STATES,
            ['wowdrone'] + self.GROUND_GROUND_STATES,
            ['wow1drone'] + self.AIR_GROUND_STATES,
            ['sportdrone'] + self.AIR_GROUND_STATES,
            ['flyaway'] + self.GROUND_GROUND_STATES,
            ['cdrone'] + self.GROUND_GROUND_STATES,
            ['ddrone'] + self.AIR_GROUND_STATES,
        ]

        self.assertTrue(len(expected_res) == len(drones_history))
        all_good = True
        for i in range(len(expected_res)):
            if not expected_res[i] == drones_history[i]:
                all_good = False
                logging.error(f'{expected_res[i]} != {drones_history[i]}')
        self.assertTrue(all_good)
