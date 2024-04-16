from model.DeliveryTruck import DeliveryTruck
from model.Delivery import Delivery
from typing import List
from random import choice, randint

class Route:
    delivery_truck: DeliveryTruck
    path: List[Delivery]
    route_id: int
    def __init__(self, delivery_truck, route_id):
        self.delivery_truck = delivery_truck
        self.path = []
        self.route_id = route_id
    
    def add(self, delivery):
        # self.delivery_truck.load(customer.demand)
        self.path.append(delivery)
    
    def get_random_delivery(self):
        return choice(self.path)

    def get_random_delivery_index(self):
        return randint(0, len(self.path))