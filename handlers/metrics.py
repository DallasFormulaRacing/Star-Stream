from datetime import datetime, timezone
from .handler import Handler 

from models import MetricDataModel

class MetricsHandler(Handler):
    async def process_event(state, data: MetricDataModel): 
        await state.conn.executemany(
            """
            INSERT INTO metrics (time, sensor_id, data) 
            VALUES ($1, $2, $3)
            """,
            [(metric.time, metric.sensor_id, metric.data) for metric in data]
        )