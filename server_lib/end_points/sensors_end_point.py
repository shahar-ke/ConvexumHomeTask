import logging
from typing import List, Tuple

from flask import Blueprint, request, jsonify

from drone_data_lib.drone_final_state import DroneFinalState
from drone_data_lib.drone_position import DronePosition
from server_lib.db_layer_lib.db_client import DBClient
from server_lib.drones_manager import DronesManager

sensors_endpoint = Blueprint('sensors_endpoint', __name__)


@sensors_endpoint.route('/sensor', methods=['POST'])
def register_sensor():
    sensor_id = request.json['sensor_id']
    sensor_id = DBClient.create_sensor(sensor_id=sensor_id)
    return jsonify({'sensor_id': sensor_id}), 200


@sensors_endpoint.route('/found', methods=['POST'])
def drone_found():
    sensor_id = request.json['sensor_id']
    drone_type = request.json['drone_type']
    drone_position = DronePosition(request.json['drone_position'])
    drone_id = DBClient.create_drone(drone_type=drone_type, drone_position=drone_position, sensor_id=sensor_id)
    drone_command = DronesManager.get_instruction(drone_id, drone_type, drone_position)
    return jsonify({'drone_id': drone_id, 'drone_command': drone_command.value}), 200


@sensors_endpoint.route('/final', methods=['POST'])
def final_drone_position():
    drone_id = request.json['drone_id']
    sensor_id = request.json['sensor_id']
    drone_position = DronePosition(request.json['drone_position'])
    drone_id = DBClient.set_final_drone_position(drone_id=drone_id, sensor_id=sensor_id, drone_position=drone_position)
    return jsonify({'drone_id': drone_id}), 200


@sensors_endpoint.route('/done', methods=['POST'])
def sensor_shutdown():
    sensor_id = request.json['sensor_id']
    drones_history: List[Tuple[int, str, DronePosition, DronePosition]] = \
        DBClient.get_sensor_drones_history(sensor_id=sensor_id)
    if len(drones_history) == 0:
        logging.info(f'sensor {sensor_id} did not sense any drones')
        return jsonify({'drones': []}), 200
    drones_history.sort(key=lambda drone_tuple: drone_tuple[0])
    logging.info(f'{sensor_id} history:')
    for drone_history in drones_history:
        initial_position = drone_history[2]
        final_position = drone_history[3]
        final_status = ''
        if initial_position == DronePosition.GROUND and final_position == DronePosition.GROUND:
            final_status = DroneFinalState.STAYED_ON_GROUND
        elif initial_position == DronePosition.GROUND and final_position == DronePosition.AIR:
            final_status = DroneFinalState.TOOK_OFF
        elif initial_position == DronePosition.AIR and final_position == DronePosition.GROUND:
            final_status = DroneFinalState.LANDED
        elif initial_position == DronePosition.AIR and final_position == DronePosition.AIR:
            final_status = DroneFinalState.STAYED_ON_AIR
        drone_id = drone_history[0]
        drone_type = drone_history[1]
        logging.info(f'drone id:{drone_id}, type:{drone_type}, '
                     f'initial position:{initial_position.value}, final position:{final_position.value}, '
                     f'final stats:{final_status.value}')
    drones_resp = [(drone_tuple[0], drone_tuple[1], drone_tuple[2].value, drone_tuple[3].value)
                   for drone_tuple in drones_history]
    return jsonify({'drones': drones_resp}), 200
