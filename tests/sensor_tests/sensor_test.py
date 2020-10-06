import logging
import os
from unittest import TestCase

from drone_data_lib.drone_position import DronePosition
from sensor_lib.drivers.sensor_driver_simulator import SensorDriverSimulator
from sensor_lib.sensor import Sensor
from tests.sensor_tests.moc_com_util import MocComUtil

logging.basicConfig(level=logging.INFO)


class SensorTest(TestCase):
    GROUND_GROUND_STATES = [DronePosition.GROUND, DronePosition.GROUND]
    AIR_GROUND_STATES = [DronePosition.AIR, DronePosition.GROUND]

    def test_sensor(self):
        demo_drones_file_path = '../../task_def/drones.txt'
        abs_drones_file_path = os.path.abspath(demo_drones_file_path)
        sensor_driver = SensorDriverSimulator(input_file_path=abs_drones_file_path, sleep_time_sec=0.1)
        com_util = MocComUtil()
        sensor = Sensor(sensor_driver=sensor_driver, com_util=com_util)
        sensor.sense()

        expected_res = {
            'Phantom3_1': self.GROUND_GROUND_STATES,
            'Mavic2_1': self.AIR_GROUND_STATES,
            'blabla_1': self.GROUND_GROUND_STATES,
            'superdrone_1': self.AIR_GROUND_STATES,
            'Phantom3_2': self.AIR_GROUND_STATES,
            'Mydrone_1': self.GROUND_GROUND_STATES,
            'parrot_1': self.AIR_GROUND_STATES,
            'newdrone_1': self.AIR_GROUND_STATES,
            'droney_1': self.GROUND_GROUND_STATES,
            'flyaway_1': self.GROUND_GROUND_STATES,
            'newdrone_2': self.AIR_GROUND_STATES,
            'airdrone_1': self.GROUND_GROUND_STATES,
            'grounddrone_1': self.AIR_GROUND_STATES,
            'd70#%_1': self.AIR_GROUND_STATES,
            'wowdrone_1': self.GROUND_GROUND_STATES,
            'wow1drone_1': self.AIR_GROUND_STATES,
            'sportdrone_1': self.AIR_GROUND_STATES,
            'flyaway_2': self.GROUND_GROUND_STATES,
            'cdrone_1': self.GROUND_GROUND_STATES,
            'ddrone_1': self.AIR_GROUND_STATES
        }

        com_util_states = com_util.DRONE_STATES
        all_good = True
        if not com_util_states == expected_res:
            for key, expected_val in expected_res.items():
                if key not in com_util_states:
                    all_good = False
                    logging.error(f'{key} is missing in result')
                    continue
                real_val = com_util_states[key]
                if expected_val != com_util_states[key]:
                    all_good = False
                    logging.error(f'{key}: {expected_val} != {real_val}')
        self.assertTrue(all_good)
