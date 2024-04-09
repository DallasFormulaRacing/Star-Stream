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
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']


app = func.FunctionApp()


@app.function_name("EventHubTrigger1")
@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="metricforwarder", cardinality="many",
                               connection="metricsforward_metricmanager_EVENTHUB")
def eventhub_processor(azeventhub: func.EventHubEvent):
    events = [json.loads(event.get_body().decode('utf-8'))
              for event in azeventhub]

    logging.info("Processing %d events; first event: %s",
                 len(events), json.dumps(events[0], indent=3))

    logging.info("Data: %s", json.dumps(events[0] if events else {}, indent=3))

    # grouping data by name
    data = {}
    for event in events:
        if event['name'] == "linpots":
            logging.info("Calculating displacements")
            calculate_displacements([event])  # wrapped it in a list to be passed to function
        name = event['name']
        if name not in data:
            data[name] = []
        data[name].append(event)

    logging.info("Created %d groups (%s)", len(data), ",".join(data.keys()))
    headers = {
        "Content-Type": "application/json"
    }

    current_ts = time.time_ns()
    logging.info("Loki Timestamp: %s\nCurrent Timestamp: %s",
                 str(events[0]['timestamp'] * 1000000000), current_ts)

    logging.info("Loki Delta: %d", current_ts -
                 events[0]['timestamp'] * 1000000000)
    post_data = {
        "streams": [
            {
                "stream": {
                    "source": name
                },
                "values": [  # this stupid conversion to nanoseconds. Who tf does logs in nanoseconds
                    [str(dump["timestamp"] * 1000000000), json.dumps(dump['fields']), dump['tags']] for dump in dumps
                ]
            } for name, dumps in data.items()
        ]
    }
    # Push to Loki
    resp = requests.post(os.environ["LOKI_URI"],
                         headers=headers, json=post_data, timeout=10)

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


def calculate_displacements(event):  # function modifies the values of the list in place then returns it

    linpot_conversion_constant = 15.0
    linpot_conversion_offset = 75.0

    event['fields']['Front Left'] = (-(event['fields']['Front Left'] * linpot_conversion_constant) +
                                     linpot_conversion_offset)
    event['fields']['Front Right'] = (-(event['fields']['Front Right'] * linpot_conversion_constant) +
                                      linpot_conversion_offset)
    event['fields']['Rear Left'] = (-(event['fields']['Rear Left'] * linpot_conversion_constant) +
                                    linpot_conversion_offset)
    event['fields']['Rear Right'] = (-(event['fields']['Rear Right'] * linpot_conversion_constant) +
                                     linpot_conversion_offset)

    return event
