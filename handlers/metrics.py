from datetime import datetime, timezone
from .handler import Handler 

from models import MetricDataModel

class MetricsHandler(Handler):
    async def process_event(state, data: MetricDataModel):
        rows_to_insert = []

        for metric in data:
            time_stamp = datetime.fromtimestamp(metric.time, tz=timezone.utc)

            rows_to_insert.append(
                (time_stamp, metric.sensor_id, metric.data)
            )
        
        await state.conn.executemany(
            """
            INSERT INTO metrics (time, sensor_id, data) 
            VALUES ($1, $2, $3)
            """,
            rows_to_insert
        )