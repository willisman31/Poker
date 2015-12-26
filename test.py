import json

class Payload:
    def __init__(self, j):
        self.__dict__ = json.loads(j)

class Student:
    def __init__(self, name, roll):
        self.name = name
        self.roll = roll

def as_payload(dct):
    return Payload(dct['action'], dct['method'], dct['data'])


message = '{"action": "safal", "obj": {"roll_number": "1", "name": "Mat"}, "data": "wow", "method": "pandita"}'
#message = json.dumps(obj, default=lambda o: o.__dict__)
print message

payload = Payload(message)
print payload.obj['name']
