import json

class Payload:
    def __init__(self, action, method, data):
        self.action = action
        self.method = method
        self.data = data

def as_payload(dct):
    return Payload(dct['action'], dct['method'], dct['data'])


obj = Payload("safal", "pandita", "wow")
message = json.dumps(obj.__dict__)
print message

payload = json.loads(message, object_hook = as_payload)
print payload.action
