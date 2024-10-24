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

class SessionStateEnum( Enum):
    OPEN = "Open"
    CLOSED = "Closed"
    ERROR = "Error"

"""
All session data
"""
# the next 3 classes are the different session models we can do, similar to how metric has 1 model, 1 event
# this time however session has 1 event and 3 models to select 
class OpenStatus (BaseModel):
    id: str #
    status: Literal["Open"]
    start: datetime
    car: str #IC24
    
class ClosedStatus(BaseModel):
    id: str
    status: Literal["Closed"]
    stop: datetime
    
class ErrorStatus(BaseModel):
    id: str
    status: Literal["Error"]
    error_name: str
    error_description: str


class SessionEvent(BaseModel):
    event_type: Literal["session"] #it MUST be session
    data: Annotated[Union[OpenStatus, ClosedStatus, ErrorStatus], Field(discriminator="status")] 




# Data(metric) Models 

class MetricModel(BaseModel):
    time: datetime 
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