import asyncio

from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient
import json 
import time 

from dotenv import load_dotenv
import os

load_dotenv()

EVENT_HUB_CONNECTION_STR = os.getenv("CONNECTION_STRING")
EVENT_HUB_NAME = "metricforwarder"


data = {
    "event": {
        "event_type": "metrics",
        "data": [
            {
                "time": time.time(),
                "sensor_id": 1,
                "data": 4.5
            },
            {
                "time": time.time(),
                "sensor_id": 1,
                "data": 5.5
            }
        ]
    }
}
data1 ={
    "event": {
        "event_type": "session",
        "data": {
            "id": "test-2",
            "status": "Closed",
            "stop": time.time()
        }
    }
}


# print(f"Sending data: {data}")
print(f"Sending data: {data1}")
#print(f"Sending data: {data1}")
async def run():
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.
    producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME
    )
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        # event_data_batch.add(EventData(json.dumps(data)))
        event_data_batch.add(EventData(json.dumps(data1)))
        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)
        print("Data sent successfully")


asyncio.run(run())
