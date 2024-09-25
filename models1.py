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

class SessionDataModel(BaseModel):
    """
    All session data
    """
    id: str
    start: datetime
    stop: Optional[datetime]
    status: SessionStateEnum
    car: str
    driver: Optional[str]

class SessionEvent(BaseModel):
    event_type: Literal["session"]
    data: SessionDataModel

# Data Models 

class MetricModel(BaseModel):
    time: datetime 
    sensor_id: int 
    data: float 

class MetricDataModel(BaseModel):
    metrics: List[MetricModel]

class MetricEvent(BaseModel):
    event_type: Literal["metrics"]

    data: MetricDataModel

# Event Model 


Event = Annotated[Union[MetricEvent, SessionEvent], Field(discriminator="event_type")]

class EventModel(BaseModel):
    event: Event