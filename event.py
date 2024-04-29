from models import Event, LinpotEvent
import logging


class Parser():
    def __init__(self, event: Event) -> None:
        self.event = event

    def parse(self) -> Event:
        if self.event["name"] == "linpot":
            DataTransformer(self.event).handle_linpot()
        if self.event["name"] == "acclgyro":
            DataTransformer(self.event).handle_acclgyro()
        if self.event["name"] == "ecu":
            DataTransformer(self.event).handle_ecu()


class DataTransformer():

    def __init__(self, event: Event):
        self.event = event

    def handle_linpot(self) -> Event:
        """
        apply displacement calculations to the event fields.
        this method is to handle all linpot transformations specifically
        """
        # for key in list of keys
        try:
            linpot_event = LinpotEvent(
                FrontLeft=self.event.fields['front_left'],
                FrontRight=self.event.fields['front_right'],
                RearLeft=self.event.fields['rear_left'],
                RearRight=self.event.fields['rear_right']
            )
            displacement_object = linpot_event.calculate_displacements_mm(self.event)
            return displacement_object

        except KeyError as e:
            logging.error("KeyError: %s", e)
            logging.error("Fields: %s", self.event.fields)
            return None

    def handle_acclgyro(self) -> Event:
        """
        apply acceleration calculations to the event fields.
        this method is to handle all acclgyro transformations specifically
        """
        pass

    def handle_ecu(self) -> Event:
        """
        apply ecu calculations to the event fields.
        this method is to handle all ecu transformations specifically
        """
        pass
