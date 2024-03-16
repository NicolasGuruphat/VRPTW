from model.DeliveryTruck import DeliveryTruck
from model.Delivery import Delivery
from typing import List

class Route:
    delivery_truck: DeliveryTruck
    path: List[Delivery]
    def __init__(self, delivery_truck):
        self.delivery_truck = delivery_truck
        self.path = []
    def add(self, delivery):
        # self.delivery_truck.load(customer.demand)
        self.path.append(delivery)