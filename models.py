# import basemodel from pydantic
#create my three classes 
# EVENT DATA SESSION ARE THE 3 CLASSES  
"""
# import basemodel from pydantic
# create my three classes 
# EVENT, DATA, SESSION ARE THE 3 CLASSES  
    ALL 3 OF THESE CLASSES ARE GOING TO INHERIT  FROM BASE MODEL(event)

    data model will have 


"""
from typing import List, Optional, Union, Literal, Dict, Any, Annotated
from enum import Enum 
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError


# Session Models 

class SessionStateEnum(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    ERROR = "error"

"""
All session data
"""
class OpenStatus (BaseModel):
    id: str #
    status: SessionStateEnum.OPEN
    start: datetime
    car: str #IC24
class ClosedStatus(BaseModel):
    id: str
    status: SessionStateEnum.CLOSED
    stop: datetime
    
class ErrorStatus(BaseModel):
    id: str
    status: SessionStateEnum.ERROR
    error_name: str
    error_description: str


class SessionEvent(BaseModel):
    event_type: Literal["session"] #it MUST be session
    data: Annotated[Union[OpenStatus, ClosedStatus, ErrorStatus], Field(discriminator="status")] 




# Data(metric) Models 

class MetricModel(BaseModel):
    time: float 
    sensor_id: int 
    data: float 

MetricDataModel = List[MetricModel] 


class MetricEvent(BaseModel):
    event_type: Literal["metrics"]

    data: MetricDataModel

# Event Model 


Event = Annotated[Union[MetricEvent, SessionEvent], Field(discriminator="event_type")]

class EventModel(BaseModel):
    event: Event