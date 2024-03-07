from model.DeliveryTruck import DeliveryTruck
from model.Customer import Customer
from typing import List

class Route:
    delivery_truck: DeliveryTruck
    path: List[Customer]
    def __init__(self, delivery_truck):
        self.delivery_truck = delivery_truck
        self.path = []
    def add(self, customer):
        self.delivery_truck.load(customer.demand)
        self.path.append(customer)