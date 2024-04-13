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
    valueFrontLeft: float
    valueFrontRight: float
    valueRearLeft: float
    valueRearRight: float


class AccelGyroEvent(BaseModel):
    '''
    Class for keeping track of accelgyro event data
    '''
    pass


class ECUEvent(BaseModel):
    '''
    Class for keeping track of ecu event data
    '''
    pass
