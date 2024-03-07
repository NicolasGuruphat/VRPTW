from datetime import datetime

class Warehouse:
    id_name: str
    x: int
    y: int
    ready_time: int
    due_time: int

    def __init__(self, id_name, x, y, ready_time, due_time):
        self.id_name = id_name
        self.x = int(x)
        self.y = int(y)
        self.ready_time = int(ready_time)
        self.due_time = int(due_time)

    def __repr__(self) -> str:
        return '{"__type": "Warehouse": "id_name":"' + self.id_name + '", "x": "' + str(self.x) + '", "y": "' + str(self.y) + '", "ready_time": "' + str(self.ready_time) + '", "due_time": "' + str(self.due_time) + '"}'