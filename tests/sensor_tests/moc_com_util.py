from collections import defaultdict
from typing import Tuple, Dict, List

from drone_data_lib.drone_command import DroneCommand
from drone_data_lib.drone_info import DroneInfo
from drone_data_lib.drone_position import DronePosition
from sensor_lib.com_utils.com_util import ComUtil


class MocComUtil(ComUtil):
    DRONE_IDS: Dict[str, int] = defaultdict(int)
    DRONE_STATES: Dict[str, List[DronePosition]] = defaultdict(list)
    DRONE_TYPES: Dict[str, str] = dict()

    @classmethod
    def get_instruction(cls, drone_info: DroneInfo, sensor_id: str) -> Tuple[str, DroneCommand]:
        cls.DRONE_IDS[drone_info.drone_type] += 1
        drone_count = cls.DRONE_IDS[drone_info.drone_type]
        drone_id = f'{drone_info.drone_type}_{drone_count}'
        cls.DRONE_TYPES[drone_id] = drone_info.drone_type
        cls.DRONE_STATES[drone_id].append(drone_info.drone_position)
        if drone_info.drone_position == DronePosition.GROUND:
            drone_command = DroneCommand.STAY_ON_GROUND
        elif drone_info.drone_position == DronePosition.AIR:
            drone_command = DroneCommand.LAND
        else:
            assert False, f'{drone_info.drone_position} is unknown drone position'
        return drone_id, drone_command

    @classmethod
    def send_final_drone_state(cls, drone_id: str, drone_info: DroneInfo, sensor_id: str):
        cls.DRONE_STATES[drone_id].append(drone_info.drone_position)

    @classmethod
    def report_done(cls, sensor_id: str):
        pass

    @classmethod
    def register_sensor(cls, sensor_id):
        pass
