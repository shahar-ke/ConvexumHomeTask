import logging
import os
from time import sleep

from drone_data_lib.drone_info import DroneInfo
from drone_data_lib.drone_position import DronePosition
from sensor_lib.drivers.sensor_driver import SensorDriver


class SensorDriverSimulator(SensorDriver):

    def __init__(self, input_file_path, sleep_time_sec: float = 3):
        super().__init__()
        assert os.path.exists(input_file_path), f'{input_file_path} not exists'
        self.input_file_path = input_file_path
        self.sleep_time_sec = sleep_time_sec

    def sense_drones(self):
        with open(self.input_file_path) as drones_file:
            for line in drones_file.readlines():
                logging.info(f'reading {line}')
                self.drones_q.put(self.line_to_drone_data(line))
                sleep(self.sleep_time_sec)

    @classmethod
    def line_to_drone_data(cls, line) -> DroneInfo:
        line = line.strip()
        line_split = line.split()
        drone_type = line_split[0]
        drone_position_str = line_split[1]
        drone_position = None
        for drone_pos in DronePosition:
            if drone_pos.value in drone_position_str or drone_position_str in drone_pos.value:
                drone_position = drone_pos
                break
        assert drone_position, f'{drone_position_str} is unknown drone position'
        drone_info = DroneInfo(drone_type=drone_type, drone_position=drone_position)
        return drone_info
