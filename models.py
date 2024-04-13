from pydantic import BaseModel
from typing import Any, Dict


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
    FrontLeft: float
    FrontRight: float
    RearLeft: float
    RearRight: float

    def calculate_displacements(self):
        constant = 15.0
        offset = 75.0

        for key in ["FrontLeft", "FrontRight", "RearLeft", "RearRight"]:
            # updating the lin pot values in place
            current_value = getattr(self, key)
            new_value = -(current_value * constant) + offset
            setattr(self, key, new_value)

    def calculate_wheel_loads():
        pass


class AccelGyroEvent(BaseModel):
    '''
    Class for keeping track of accelgyro event data
    '''
    def calculate_acceleration():
        pass

    pass


class ECUEvent(BaseModel):
    '''
    Class for keeping track of ecu event data
    '''
    pass
