from models import Event


class Transform():

    def __init__(self, event: Event):
        self.event = event

    def calculate_linpot_displacements(self):
        """
        apply displacement calculations to the event fields.
        """
        constant = 15.0
        offset = 75.0
        # for key in list of keys
        for key in ['Front Left', 'Front Right', 'Rear Left', 'Rear Right']:

            # check if the key is in the feilds dict
            if key in self.event.fields:
                # update the value of the key in the feilds dict
                self.event.fields[key] = -(self.event.fields[key] * constant) + offset
