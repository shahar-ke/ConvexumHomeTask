from drone_data_lib.drone_position import DronePosition


class DroneInfo:

    def __init__(self, drone_type: str, drone_position: DronePosition):
        self.drone_type = drone_type
        self.drone_position = drone_position
