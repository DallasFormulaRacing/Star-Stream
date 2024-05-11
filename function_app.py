from event import DataTransformer as DT
from event import Parser
from datetime import datetime
import azure.functions as func
import logging
import os
import requests
import time
from pymongo import MongoClient
import certifi
import json
import dns.resolver
from can import Message
from data_deserializer import MessageData
from event import DataTransformer, Parser
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']


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

    # group all events that have the same event['tasg']
    for event in events:

        Parser(event).parse()

        if event["tags"].get("source", "") == "ecu":
            arbitration_id = event["fields"].get("id", 0)
            raw_data = event["fields"].get("data", "")
            timestamp = event["timestamp"]

            # parsing data
            data_strings = raw_data.split(" ")
            ecu_data = [int(data_string, 16) for data_string in data_strings]
            msg = Message(timestamp=timestamp, arbitration_id=arbitration_id, data=ecu_data)
            msg_data = MessageData(msg)
            try:
                event["fields"] = json.loads(json.dumps(msg_data.to_dict(), default=str))
            except Exception:  # TODO: Make this a specific exception
                logging.error("[ECU] Error converting to dict: %s", msg)
                continue
        elif event["tags"].get("source", "") == "linpot":
            
        tags = event['tags']

        # Call frozen set because we can't hash a dictionary
        tags_key = frozenset(tags.items())
        if tags_key not in data:
            data[tags_key] = []

        data[tags_key].append(event)

    logging.info("Created %d groups", len(data))
    headers = {
        "Content-Type": "application/json"
    }

    current_ts = time.time_ns()
    logging.info("Loki Timestamp: %s\nCurrent Timestamp: %s", str(events[0]['timestamp'] * 1000000), current_ts)

    logging.info("Loki Delta: %d", current_ts - events[0]['timestamp'] * 1000000)
    post_data = {
        "streams": [
            {
                "stream": {k: v for (k, v) in tags},
                "values": [  # this stupid conversion to nanoseconds. Who tf does logs in nanoseconds
                    [str(dump["timestamp"] * 1000000), json.dumps(dump['fields'], default=str)] for dump in dumps
                ]
            } for tags, dumps in data.items()
        ]
    }
    # Push to Loki
    resp = requests.post(os.environ["LOKI_URI"], headers=headers, json=post_data, timeout=10)

    if resp.status_code != 204:
        logging.error("Error pushing to Loki: %s\n\nData; %s",
                      resp.text, json.dumps(post_data, indent=3))
    else:
        logging.info("Pushed to Loki with status %d: %s",
                     resp.status_code, resp.content)

    client = MongoClient(os.environ["MONGO_URI"], tlsCAFile=certifi.where())
    # Push to MongoDB
    db = client["cluster0"]

    documents = []
    for doc in events:
        doc = {
            "metadata": doc['tags'],
            "timestamp": datetime.fromtimestamp(doc['timestamp'] / 1000),
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
