from model.VRPTW import VRPTW
from model.DeliveryTruck import DeliveryTruck
from model.Route import Route
from model.Delivery import Delivery
import random as r
import math
from printer.printer import display_vrp
from utils import get_time_between, switch_two_deliveries_in_same_route
from typing import List
VRPTW_ = VRPTW('data111.vrp')

totalServiceTime = 0

for customers in VRPTW_.customers:
    totalServiceTime += customers.service

minTruckNumber = math.ceil((totalServiceTime) / (VRPTW_.warehouse.due_time - VRPTW_.warehouse.ready_time))
minTruckNumber += 5 # To remove

trucks = []
routes: List[Route] = []

for i in range(minTruckNumber):
    delivery_truck = DeliveryTruck(VRPTW_.truck_package_limit)
    trucks.append(delivery_truck)
    routes.append(Route(delivery_truck, i))
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
        and current_time + get_time_between(last_delivery_x, last_delivery_y, VRPTW_.warehouse.x, VRPTW_.warehouse.y) < VRPTW_.warehouse.due_time
        ): 
        for customer in customers_left:
            if (
                (customer.ready_time <= current_time + (d:= get_time_between(last_delivery_x, last_delivery_y, customer.x, customer.y))
                and customer.due_time >= current_time + d)
                and current_time + d + customer.service + get_time_between(VRPTW_.warehouse.x, VRPTW_.warehouse.y, customer.x, customer.y) <=  VRPTW_.warehouse.due_time
                and customer.demand <= current_truck.package_left
            ):
                # on met le customer dans la route
                delivery = Delivery(customer, last_delivery_time + get_time_between(last_delivery_x, last_delivery_y, customer.x, customer.y))
                route.add(delivery)
                last_delivery_x = customer.x
                last_delivery_y = customer.y
                last_delivery_time = route.path[-1].departure
                current_truck.load(customer.demand)
                current_time = delivery.departure
                customers_left.pop(customers_left.index(customer))
        if(current_truck.package_left > 0 and current_time < VRPTW_.warehouse.due_time):
            # ajouter le * 0.8 au dessus
            # on ajoute du temps pour éviter que le camion attende indéfiniment
            current_time += 1
        
    if(len(customers_left) == 0):
        break

display_vrp(VRPTW_.warehouse, VRPTW_.customers, routes)

print(routes[0].path)
switch_two_deliveries_in_same_route(routes[0], 0, 1, VRPTW_.warehouse)
print(routes[0].path)

r1 = []
r2 = []
for route in routes:
    l = len(r2)
    r1.extend([e.is_on_time for e in route.path])
    r2.extend([e for e in route.path if not e.is_on_time])
    if l != len(r2):
        print(routes.index(route))
print(f"Works: {all(r1)}")
print(f"Not working count: {len(r2)}")
print(r2)
# display_vrp(VRPTW_.warehouse, VRPTW_.customers, routes)
