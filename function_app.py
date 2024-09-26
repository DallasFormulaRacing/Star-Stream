from typing import List

from models import EventModel, Event
import azure.functions as func
import logging
import json
from state import State

app = func.FunctionApp()

state.cold_init()

@app.function_name("EventHubTrigger1")
@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="metricforwarder", cardinality="many",
                               connection="metricsforward_metricmanager_EVENTHUB")
async def eventhub_processor(azeventhub: func.EventHubEvent):


    # pass incoming events into the event class
    events = [json.loads(event.get_body().decode('utf-8'))
              for event in azeventhub]


    logging.info("Processing %d events; first event: %s",
                 len(events), json.dumps(events[0], indent=3))
    logging.info("Data: %s", json.dumps(events[0] if events else {}, indent=3))

