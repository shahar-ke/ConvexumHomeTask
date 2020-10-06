from sqlalchemy.exc import IntegrityError

from drone_data_lib.drone_position import DronePosition
from server_lib.db_layer_lib.database import db
from server_lib.db_layer_lib.models.drone_model import DroneModel, DronePositionModel
from server_lib.db_layer_lib.models.sensor_model import SensorModel


class DBClient:

    @classmethod
    def create_sensor(cls, sensor_id: str):
        try:
            sensor = SensorModel(id=sensor_id)
            db.session.add(sensor)
            db.session.commit()
            return sensor.id
        except IntegrityError:
            # in case multiple requests for new sensor at same time
            db.session.rollback()
            return sensor_id

    @classmethod
    def create_drone(cls, drone_type: str, drone_position: DronePosition, sensor_id: str):
        drone = DroneModel(drone_type=drone_type, sensor_id=sensor_id)
        db.session.add(drone)
        db.session.commit()
        drone.drone_positions.append(DronePositionModel(position=drone_position.value))
        db.session.commit()
        return drone.id

    @classmethod
    def set_final_drone_position(cls, drone_id: int, sensor_id: str, drone_position: DronePosition):
        drone = DroneModel.query.with_for_update(of=DroneModel, nowait=True).filter_by(id=drone_id,
                                                                                       sensor_id=sensor_id).first()
        assert drone and len(drone.drone_positions) == 1
        drone.drone_positions.append(DronePositionModel(position=drone_position.value))
        db.session.commit()
        return drone.id

    @classmethod
    def get_sensor_drones_history(cls, sensor_id):
        drones = DroneModel.query.filter_by(sensor_id=sensor_id).all()
        drones_history = list()
        for drone in drones:
            if len(drone.drone_positions) != 2:
                continue
            initial_position = DronePosition(drone.drone_positions[0].position)
            final_position = DronePosition(drone.drone_positions[1].position)
            drones_history.append((drone.id, drone.drone_type, initial_position, final_position))
        return drones_history
