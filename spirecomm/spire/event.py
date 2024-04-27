class Event:

    def __init__(self, event_id, name, counter=0, price=0):
        self.event_id = event_id
        self.name = name
        self.counter = counter
        self.price = price

    @classmethod
    def from_json(cls, json_object):
        return cls(json_object["id"], json_object["name"], json_object["counter"], json_object.get("price", 0))
