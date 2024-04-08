from datetime import datetime
import azure.functions as func
import logging
import os
import requests
from pymongo import MongoClient
import certifi 

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

try:
    import orjson as json
except ImportError:
    import json

app = func.FunctionApp()

@app.function_name("EventHubTrigger1")
@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="metricforwarder", cardinality="many",
                               connection="metricsforward_metricmanager_EVENTHUB") 
def eventhub_processor(azeventhub: func.EventHubEvent):    
    events = [json.loads(event.get_body().decode('utf-8')) for event in azeventhub]
    
    logging.info("Processing %d events; first event: %s", len(events), json.dumps(events[0], indent=3))
    
    logging.info("Data: %s", json.dumps(events[0] if events else {}, indent=3))
    
    # grouping data by name 
    data = {}
    for event in events:
        name = event['name']
        if name not in data:
            data[name] = []
        data[name].append(event)
    
    logging.info("Created %d groups (%s)", len(data), ",".join(data.keys()))
    headers = {
        "Content-Type": "application/json"
    }
    
    post_data = {
        "streams": [
            {
                "stream": {
                    "source": name
                },
                "values": [ # this stupid conversion to nanoseconds. Who tf does logs in nanoseconds
                    [str(dump["timestamp"] * 1000000000), json.dumps(dump['fields']), dump['tags']] for dump in dumps
                ]
            } for name, dumps in data.items()
        ]
    }
    # Push to Loki
    resp = requests.post(os.environ["LOKI_URI"], headers=headers, json=post_data)
    
    if resp.status_code != 204:
        logging.error("Error pushing to Loki: %s\n\nData; %s", resp.text, json.dumps(post_data, indent=3))
    else:
        logging.info("Pushed to Loki with status %d", resp.status_code)
    
    client = MongoClient(os.environ["MONGO_URI"], tlsCAFile=certifi.where())
    # Push to MongoDB
    db = client["cluster0"]
    
    documents = []
    for doc in events:
        doc = {
                "metadata": doc['tags'],
                "timestamp": datetime.fromtimestamp(doc['timestamp']),
                **doc['fields']
            }

        # validate timestamp because they suck
        if doc['timestamp'] > datetime.now() or doc['timestamp'] < datetime(2020, 1, 1):
            logging.error("Invalid timestamp: %s", doc['timestamp'])
            raise ValueError("Invalid timestamp")
        
        documents.append(doc)
        
    db.realtime_metrics.insert_many(documents)
    
    logging.info("Pushed to MongoDB")
    
    client.close()