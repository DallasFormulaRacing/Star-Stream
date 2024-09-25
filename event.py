from models import Event, LinpotEvent
import logging
from pydantic import ValidationError


class Parser():
    def __init__(self, event: Event) -> None:
        self.event = event

    def parse(self) -> None:
        try:
            if self.event["name"] == "linpot":
                DataTransformer(self.event).handle_linpot()
            elif self.event["name"] == "accel":
                DataTransformer(self.event).handle_acclgyro()
            elif self.event["name"] == "gyro":
                DataTransformer(self.event).handle_acclgyro()
        except Exception as e:
            logging.error("Error: %s, event not identifiable", e)


class DataTransformer():

    def __init__(self, event: Event):
        self.event = event

    def handle_linpot(self) -> LinpotEvent:
        """
        apply displacement calculations to the event fields.
        this method is to handle all linpot transformations specifically
        """
        try:
            linpot_event = LinpotEvent(
                fields={
                    'front_left': self.event.fields['front_left'],
                    'front_right': self.event.fields['front_right'],
                    'rear_left': self.event.fields['rear_left'],
                    'rear_right': self.event.fields['rear_right']
                },
                name=self.event.name,
                tags=self.event.tags,
                timestamp=self.event.timestamp
            )
            displacement_object = linpot_event.calculate_displacements_mm(self.event)
            return displacement_object

        except Exception as e:
            logging.error("Error: %s", e)
            logging.error("Fields: %s", self.event.fields)
            return None

    def handle_acclgyro(self) -> Event:
        """
        apply acceleration calculations to the event fields.
        this method is to handle all acclgyro transformations specifically
        """
        pass
