import logging
import random
import string
from time import sleep

from drone_data_lib.drone_command import DroneCommand
from drone_data_lib.drone_info import DroneInfo
from drone_data_lib.drone_position import DronePosition
from sensor_lib.com_utils.com_util import ComUtil
from sensor_lib.com_utils.http_com_util import HTTPComUtil
from sensor_lib.drivers.sensor_driver import SensorDriver
from sensor_lib.drivers.sensor_driver_simulator import SensorDriverSimulator

logging.basicConfig(level=logging.INFO)


class Sensor:

    def __init__(self, sensor_driver: SensorDriver, com_util: ComUtil):
        self.sensor_driver: SensorDriver = sensor_driver
        self.com_util: ComUtil = com_util
        self.sensor_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

    # while driver is active, sense drones, ask server for instruction, handle it, and report result
    def sense(self):
        self.sensor_driver.start()
        self.register()
        # while driver is active
        while self.sensor_driver.active():
            # sense drones (sensor driver is async)
            while self.sensor_driver.drone_sensed():
                drone_info: DroneInfo = self.sensor_driver.get_sensed_drone()
                # ask for instruction
                drone_id, drone_command = self.com_util.get_instruction(drone_info=drone_info,
                                                                        sensor_id=self.sensor_id)
                # handle instruction
                self.handle_instruction(drone_info, drone_command)
                # report result
                self.com_util.send_final_drone_state(drone_id=drone_id,
                                                     drone_info=drone_info,
                                                     sensor_id=self.sensor_id)
            # avoiding busy wait, in case sense driver is active but do not sense anything at the moment
            sleep(0.1)
        return self.com_util.report_done(sensor_id=self.sensor_id)

    # handle instruction and update drone info with updated state
    @classmethod
    def handle_instruction(cls, drone_info: DroneInfo, drone_command: DroneCommand):
        if drone_command == DroneCommand.STAY_ON_GROUND:
            drone_info.drone_position = DronePosition.GROUND
        elif drone_command == DroneCommand.LAND:
            drone_info.drone_position = DronePosition.GROUND
        else:
            assert False, f'{drone_command} unsupported command'

    # for supporting multiple sensors scenario
    def register(self):
        self.com_util.register_sensor(sensor_id=self.sensor_id)


def main():
    com_util = HTTPComUtil()
    sensor_driver = SensorDriverSimulator(input_file_path='../task_def/drones.txt', sleep_time_sec=0.1)
    sensor = Sensor(sensor_driver=sensor_driver, com_util=com_util)
    sensor.sense()


if __name__ == '__main__':
    main()
