from enum import Enum


class DroneFinalState(Enum):
    STAYED_ON_GROUND = 'Stayed on ground'
    TOOK_OFF = 'Took off'
    LANDED = 'Landed'
    STAYED_ON_AIR = 'Stayed on air'
