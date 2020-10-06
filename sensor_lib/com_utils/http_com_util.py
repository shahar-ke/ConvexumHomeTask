from typing import Tuple, Dict

import requests

from drone_data_lib.drone_command import DroneCommand
from drone_data_lib.drone_info import DroneInfo
from sensor_lib.com_utils.com_util import ComUtil


class HTTPComUtil(ComUtil):

    def __init__(self, host_url: str = 'http://localhost:5000'):
        self.host_url: str = host_url

    # returns instructions for a newly found drone
    def get_instruction(self, drone_info: DroneInfo, sensor_id: str) -> Tuple[str, DroneCommand]:
        url = f'{self.host_url}/found'
        data = self._pack_data(drone_info=drone_info, sensor_id=sensor_id)
        response = requests.post(url, json=data)
        resp_json = response.json()
        drone_command = DroneCommand(resp_json['drone_command'])
        drone_id = resp_json['drone_id']
        return drone_id, drone_command

    def send_final_drone_state(self, drone_id: str, drone_info: DroneInfo, sensor_id: str):
        url = f'{self.host_url}/final'
        data = self._pack_data(drone_info=drone_info, sensor_id=sensor_id, drone_id=drone_id)
        data['drone_id'] = drone_id
        response = requests.post(url, json=data)
        assert response.status_code == 200
        return response.json()

    def report_done(self, sensor_id: str):
        url = f'{self.host_url}/done'
        data = self._pack_data(sensor_id=sensor_id)
        response = requests.post(url, json=data)
        assert response.status_code == 200
        return response.json()

    @classmethod
    def _pack_data(cls, sensor_id: str, drone_info: DroneInfo = None, drone_id: str = None) -> Dict[str, str]:
        data = {'sensor_id': sensor_id}
        if drone_info:
            data['drone_type'] = drone_info.drone_type
            data['drone_position'] = drone_info.drone_position.value
        if drone_id:
            data['drone_id'] = drone_id
        return data

    def register_sensor(self, sensor_id):
        url = f'{self.host_url}/sensor'
        data = self._pack_data(sensor_id=sensor_id)
        response = requests.post(url, json=data)
        assert response.status_code == 200
        return response.json()
