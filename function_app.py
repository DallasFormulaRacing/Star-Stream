from typing import List, Dict

from models import EventModel, Event
from itertools import groupby
from pydantic import ValidationError
from handlers import Handler, SessionHandler, MetricsHandler
import azure.functions as func
import logging
import json
import os 
from traceback import print_exc 

from state import State

app = func.FunctionApp()

state = State(
    pg_uri = os.getenv("POSTGRES_URI")
)

handlers: Dict[str, Handler] = {
    "session": SessionHandler,
    "metrics": MetricsHandler,
}

@app.function_name("EventHubTrigger1")
@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="metricforwarder", cardinality="many",
                               connection="metricsforward_metricmanager_EVENTHUB", consumer_group=os.getenv("GROUP_ID"))
async def eventhub_processor(azeventhub: func.EventHubEvent):

    # pass incoming events into the event azu
    events = [json.loads(event.get_body().decode('utf-8'))
              for event in azeventhub]

    logging.info("Processing %d events; first event: %s",
                 len(events), json.dumps(events[0], indent=3))
    logging.info("Data: %s", json.dumps(events[0] if events else {}, indent=3))

    # connect to our databases
    await state.setup()

    # event validation
    event_models = []
    async with state.conn.transaction():
        for event in events:
            try:
                model = EventModel(**event)
            except ValidationError as exc:
                logging.error("Error %s while decoding Event Model: %s", type(exc), str(exc))
                print_exc() # trace logging
                raise 
            
            event = model.event
            if handler := handlers.get(event.event_type):
                await handler.process_event(state, event.data)
