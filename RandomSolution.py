from model.VRPTW import VRPTW
from model.DeliveryTruck import DeliveryTruck
from model.Route import Route
from model.Delivery import Delivery
import random as r
import math
from printer.printer import display_vrp
from utils import get_time_between
from typing import List
VRPTW_ = VRPTW('data111.vrp')

totalServiceTime = 0

for customers in VRPTW_.customers:
    totalServiceTime += customers.service

minTruckNumber = math.ceil((totalServiceTime) / (VRPTW_.warehouse.due_time - VRPTW_.warehouse.ready_time))
minTruckNumber += 5 # To remove

trucks = []
routes: List[Route] = []

for _ in range(minTruckNumber):
    delivery_truck = DeliveryTruck(VRPTW_.truck_package_limit)
    trucks.append(delivery_truck)
    routes.append(Route(delivery_truck))
customers_left = VRPTW_.customers.copy()
for route in routes:
    # assignation des 
    picked_truck = r.randint(0,len(trucks)-1)
    route.truck = trucks[picked_truck] 
    current_truck = route.truck
    trucks.pop(picked_truck)
    current_time = 0
    last_delivery_x = VRPTW_.warehouse.x
    last_delivery_y = VRPTW_.warehouse.y
    last_delivery_time = 0
    while(
        current_truck.package_left > 0 # current_truck.package_limit # * 0.8 # on ne remplit les camions qu'à 80%
        and len(customers_left) > 0 
        and current_time < VRPTW_.warehouse.due_time
        ): 
        for customer in customers_left:
            if (
                customer.ready_time >= current_time 
                and current_time + customer.service <=  VRPTW_.warehouse.due_time
                and customer.demand <= current_truck.package_left
            ):
                # on met le customer dans la route
                route.add(Delivery(customer, last_delivery_time + get_time_between(last_delivery_x, last_delivery_y, customer.x, customer.y)))
                last_delivery_x = customer.x
                last_delivery_y = customer.y
                last_delivery_time = route.path[-1].departure
                current_truck.load(customer.demand)
                current_time += customer.service
                customers_left.pop(customers_left.index(customer))
        if(current_truck.package_left > 0 and current_time < VRPTW_.warehouse.due_time):
            # ajouter le * 0.8 au dessus
            # on ajoute du temps pour éviter que le camion attende indéfiniment
            current_time += 1
        
    if(len(customers_left) == 0):
        break

display_vrp(VRPTW_.warehouse, VRPTW_.customers, routes)