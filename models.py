from pydantic import BaseModel, ValidationError 
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
    front_left: float
    front_right: float
    rear_left: float
    rear_right: float

    def calculate_displacements_mm(self, event: Event)-> Event:
        """calcualtes displacements in mm from linpot values

        Returns:
            dict: displacements in mm
        """

        displacements = {}
        linpots = ["front_left", "front_right", "rear_left", "rear_right"]

        for key in linpots:
            current_value = getattr(self, key)
            converted_to_mm = -(current_value * LINPOT_CONVERSION_CONSTANT) + LINPOT_CONVERSION_OFFSET
            displacements[key] = converted_to_mm

        event.fields.update(displacements)
        
        return event

    def calculate_wheel_loads(self):
        pass


class AccelGyroEvent(BaseModel):
    '''
    Class for keeping track of accelgyro event data
    '''
    def calculate_gforce():
        pass



class ECUEvent(BaseModel):
    '''
    Class for keeping track of ecu event data
    '''
    pass
