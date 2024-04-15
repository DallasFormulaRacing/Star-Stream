from pydantic import BaseModel
from typing import Any, Dict

LINPOT_CONVERSION_CONSTANT = 15.0
LINPOT_CONVERSION_OFFSET = 75.0
MM_TO_IN_CONVERSION_FACTOR = 0.0393701


class Event(BaseModel):
    '''
    Class for keeping track of the event data
    '''
    name: str
    fields: Dict[str, Any]
    tags: Dict[str, Any]
    timestamp: float


class LinpotEvent(BaseModel):
    '''
    Class for keeping track of linpot event data
    '''
    # TODO rename the values for front left, front right, rear left, rear right and so on to not have spaces
    front_left: float
    front_right: float
    rear_left: float
    rear_right: float

    def calculate_displacements_mm(self):
        for key in ["Front Left", "Front Right", "Rear Left", "Rear Right"]:
            # updating the lin pot values in place
            current_value = getattr(self, key)
            new_value = -(current_value * LINPOT_CONVERSION_CONSTANT) + LINPOT_CONVERSION_OFFSET
            setattr(self, key, new_value)

    def calculate_wheel_loads():
        pass


class AccelGyroEvent(BaseModel):
    '''
    Class for keeping track of accelgyro event data
    '''
    def calculate_gforce():
        pass

    pass


class ECUEvent(BaseModel):
    '''
    Class for keeping track of ecu event data
    '''
    pass
