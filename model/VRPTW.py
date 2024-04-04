from typing import List
from model.Customer import Customer
from model.DeliveryTruck import DeliveryTruck
from model.Warehouse import Warehouse
from model.Route import Route
from Parser import parse_vrptw_file
from random import choice

class VRPTW:

    customers: List[Customer]
    deliveryTrucks: List[DeliveryTruck]
    warehouse: Warehouse
    routes: List[Route]
    truck_package_limit: int
    def __init__(self, file_name):
        (   
            _,
            warehouse_number,
            customer_number,
            truck_package_limit, 
            warehouses,
            customers
        ) = parse_vrptw_file('data/'+file_name)
        self.truck_package_limit = truck_package_limit
        self.warehouse = warehouses[0]
        self.customers = customers
        self.deliveryTrucks = []
        self.routes = []
        
    def get_random_route(self):
        return choice(self.routes)