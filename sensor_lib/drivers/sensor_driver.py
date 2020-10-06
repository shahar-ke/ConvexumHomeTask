import logging
import queue
from abc import ABC
from threading import Thread


# base class for driver threads
class SensorDriver(Thread, ABC):

    def __init__(self):
        super().__init__()
        self.drones_q = queue.Queue()
        self.activated = False

    def run(self):
        self.activated = True
        try:
            self.sense_drones()
        except Exception as e:
            logging.exception(f'caught {str(e)} while sensing drones')
        finally:
            self.activated = False

    def active(self):
        return self.activated

    def drone_sensed(self):
        return self.drones_q.qsize() > 0

    def get_sensed_drone(self):
        assert self.drones_q.qsize() > 0, 'please verify drone_sensed first'
        return self.drones_q.get()

    def sense_drones(self):
        raise NotImplementedError()
