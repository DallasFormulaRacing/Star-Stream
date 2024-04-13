from models import Event, LinpotEvent
import logging


class DataTransformer():

    def __init__(self, event: Event):
        self.event = event

    def handle_linpot(self) -> Event:
        """
        apply displacement calculations to the event fields.
        this method is to handle linpot specifically
        """
        # for key in list of keys
        try:
            linpot_event = LinpotEvent(
                FrontLeft=self.event.fields['Front Left'],
                FrontRight=self.event.fields['Front Right'],
                RearLeft=self.event.fields['Rear Left'],
                RearRight=self.event.fields['Rear Right']
            )
            event = linpot_event.calculate_displacements()
            return event
        except KeyError as e:
            logging.error("KeyError: %s", e)
            logging.error("Fields: %s", self.event.fields)
            return
