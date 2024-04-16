from model.VRPTW import VRPTW
from model.DeliveryTruck import DeliveryTruck
from model.Route import Route
from model.Delivery import Delivery
from model.Customer import Customer
import random as r
import math
from printer.printer import display_vrp
from utils import get_time_between, switch_two_deliveries_in_same_route, switch_two_deliveries
from typing import List
VRPTW_ = VRPTW('data111.vrp')
# VRPTW_ = VRPTW('data_test.vrp')

totalServiceTime = 0

for customers in VRPTW_.customers:
    totalServiceTime += customers.service

minTruckNumber = math.ceil((totalServiceTime) / (VRPTW_.warehouse.due_time - VRPTW_.warehouse.ready_time))
minTruckNumber += 5 # To remove

trucks = []
routes: List[Route] = []

# for _ in range(minTruckNumber):
#     delivery_truck = DeliveryTruck(VRPTW_.truck_package_limit)
#     trucks.append(delivery_truck)
#     routes.append(Route(delivery_truck))

customers_left = VRPTW_.customers.copy()
i = -1
while customers_left:
    i += 1
    current_truck = DeliveryTruck(VRPTW_.truck_package_limit)
    trucks.append(current_truck)
    current_route = Route(current_truck, i)
    routes.append(current_route)

    exist_reachable_customers = True

    last_delivery_x = VRPTW_.warehouse.x
    last_delivery_y = VRPTW_.warehouse.y
    last_delivery_time = 0

    while exist_reachable_customers:
        reachable_customers: List[Customer] = list()
        too_early_customers:  List[Customer] = list()

        for customer in customers_left:
            time_for_distance = get_time_between(last_delivery_x, last_delivery_y, customer.x, customer.y)
            time_to_get_back_to_warehouse = get_time_between(VRPTW_.warehouse.x, VRPTW_.warehouse.y, customer.x, customer.y)
            estimated_arrival = last_delivery_time + time_for_distance
            if (
                customer.due_time >= estimated_arrival
                and customer.demand <= current_truck.package_left
                and time_to_get_back_to_warehouse + max(last_delivery_time + time_for_distance, customer.ready_time) + customer.service <= VRPTW_.warehouse.due_time
            ):
                if customer.ready_time <= estimated_arrival:
                    reachable_customers.append(customer)
                else:
                    too_early_customers.append(customer)

        # print(f"R: {reachable_customers}\nE: {too_early_customers}")

        if reachable_customers:
            next_customer = reachable_customers[r.randint(0, len(reachable_customers) - 1)]
            arrival = last_delivery_time + get_time_between(last_delivery_x, last_delivery_y, next_customer.x, next_customer.y)
            # print(f"T: {len(trucks)} {current_truck.package_left} --- CL: {len(customers_left)} --- Reach: {next_customer.id_name} {next_customer.ready_time} {next_customer.due_time} --- A: {arrival} --- R: {len(current_route.path)}")
        elif too_early_customers:
            next_customer = too_early_customers[r.randint(0, len(too_early_customers) - 1)]
            arrival = next_customer.ready_time
            # print(f"T: {len(trucks)} {current_truck.package_left} --- CL: {len(customers_left)} --- Early: {next_customer.id_name} {next_customer.ready_time} {next_customer.due_time} --- A: {arrival} --- R: {len(current_route.path)}")
        else:
            exist_reachable_customers = False
            continue

        delivery = Delivery(next_customer, arrival)
        current_route.add(delivery)
        last_delivery_x = next_customer.x
        last_delivery_y = next_customer.y
        last_delivery_time = delivery.departure
        current_truck.load(next_customer.demand)
        customers_left.pop(customers_left.index(next_customer))
    
    if len(current_route.path) <= 0 and customers_left:
        raise ValueError("VRPTW may have no solution")


display_vrp(VRPTW_.warehouse, VRPTW_.customers, routes)

# print(routes[0].path)

r1 = []
r2 = []
for route in routes:
    l = len(r2)
    r1.extend([e.is_on_time for e in route.path])
    r2.extend([e for e in route.path if not e.is_on_time])
    # if l != len(r2):
    #     print(routes.index(route))
print(f"Works: {all(r1)}")
print(f"Not working count: {len(r2)}")
cop = routes[0].path.copy()
print(routes[0].path)
switch_two_deliveries(routes, routes[0].path[0], routes[0].path[1], VRPTW_.warehouse)
print(routes[0].path)
# switch_two_deliveries_in_same_route(routes[0], 0, 1, VRPTW_.warehouse)
print(f"Switch : {routes[0].path != cop}")
# print(r2)
display_vrp(VRPTW_.warehouse, VRPTW_.customers, routes)
