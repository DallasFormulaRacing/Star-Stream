from dataclasses import dataclass
from tpying import Dict, Any


@dataclass
class Event():
    name: str
    feilds: Dict[str, Any]
    tags: Dict[str, Any]
    timestamp: float

    def calculate_displacements(self) -> None:
        """
        apply displacement calculations to the event fields.
        """
        constant = 15.0
        offset = 75.0

        for key in ['Front Left', 'Front Right', 'Rear Left', 'Rear Right']:
            if key in self.fields:
                self.fields[key] = -(self.fields[key] * constant) + offset

    @staticmethod
    def from_json(json_data: Dict[str, Any]):
        """
        create an event object from a json object
        """
        return Event(
            name=json_data["name"],
            fields=json_data["fields"],
            tags=json_data["tags"],
            timestamp=json_data["timestamp"]
        )
