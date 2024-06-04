
class Customer:
    id_name: str 
    x: int
    y: int
    ready_time: int
    due_time: int
    demand : int
    service: int

    def __init__(self, id_name, x, y, ready_time, due_time, demand, service):
        self.id_name = id_name
        self.x = int(x)
        self.y = int(y)
        self.ready_time = 0
        self.due_time = 230
        # self.ready_time = int(ready_time)
        # self.due_time = int(due_time)
        self.demand = int(demand)
        self.service = int(service)
    
    def __repr__(self) -> str:
        return '{"__type": "Customer", "id_name":"' + self.id_name + '", "x": "' + str(self.x) + '", "y": "' + str(self.y) + '", "ready_time": "' + str(self.ready_time) + '", "due_time": "' + str(self.due_time) + '", "demand": "' + str(self.demand) + '", "service": "' + str(self.service) + '"}'
    
    def __eq__(self, value: object) -> bool:
        return isinstance(value, Customer) and value.id_name == self.id_name