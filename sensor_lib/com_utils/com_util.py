from abc import ABC
from typing import Tuple

from drone_data_lib.drone_command import DroneCommand
from drone_data_lib.drone_info import DroneInfo


class ComUtil(ABC):

    # sends server drone info and respond with instructions and drone id to be used in later calls
    def get_instruction(self, drone_info: DroneInfo, sensor_id: str) -> Tuple[str, DroneCommand]:
        raise NotImplementedError()

    # report to server instructions results for drone id
    def send_final_drone_state(self, drone_id: str, drone_info: DroneInfo, sensor_id: str):
        raise NotImplementedError()

    # reports to server registered sensor is done
    def report_done(self, sensor_id: str):
        raise NotImplementedError()

    # registers a sensor with server
    def register_sensor(self, sensor_id):
        raise NotImplementedError()
