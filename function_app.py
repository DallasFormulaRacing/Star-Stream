import azure.functions as func
import logging
import os
import requests
try:
    import orjson as json
except ImportError:
    import json

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


app = func.FunctionApp()

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="metricforwarder",
                               connection="metricsforward_metricmanager_EVENTHUB") 
def eventhub_processor(azeventhub: func.EventHubEvent):
    body = azeventhub.get_body().decode('utf-8')
    logging.info('Python EventHub trigger processed an event: %s',
                body)
    
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        logging.error("Error decoding JSON")
        return
    
    # Push to Loki
    requests.post("http://loki:3100/loki/api/v1/push", json=data)
    
    # Push to MongoDB