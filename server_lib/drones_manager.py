from drone_data_lib.drone_command import DroneCommand
from drone_data_lib.drone_position import DronePosition


class DronesManager:
    # noinspection PyUnusedLocal
    @classmethod
    def get_instruction(cls, drone_id, drone_type, drone_position) -> DroneCommand:
        if drone_position == DronePosition.GROUND:
            return DroneCommand.STAY_ON_GROUND
        if drone_position == DronePosition.AIR:
            return DroneCommand.LAND
