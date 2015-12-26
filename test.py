import json

class Student:
    def __init__(self, name = "Mat", roll_number = "1"):
        self.name = name
        self.roll_number = roll_number

class Payload:
    def __init__(self, action, method, data):
        self.action = action
        self.method = method
        self.data = data
        self.obj = Student()
def as_payload(dct):
    return Payload(dct['action'], dct['method'], dct['data'], dct['obj'])


obj = Payload("safal", "pandita", "wow")
message = json.dumps(obj, default=lambda o: o.__dict__)
print message
print obj.obj.name
#
# payload = json.loads(message, object_hook = as_payload)
# print payload.action
