from typing import List
import random as r
import math

from model.VRPTW import VRPTW
from model.Route import Route
from model.Customer import Customer
from model.Delivery import Delivery
from model.DeliveryTruck import DeliveryTruck

from utils import get_time_between

def random_solution(vrptw: VRPTW) -> List[Route]:
    customers_left: list = vrptw.customers.copy()
    trucks = list()
    routes = list()
    i = -1
    while customers_left:
        i += 1
        current_truck = DeliveryTruck(vrptw.truck_package_limit)
        trucks.append(current_truck)
        current_route = Route(current_truck, i)
        routes.append(current_route)

        exist_reachable_customers = True

        last_delivery_x = vrptw.warehouse.x
        last_delivery_y = vrptw.warehouse.y
        last_delivery_time = 0

        while exist_reachable_customers:
            reachable_customers: List[Customer] = list()
            too_early_customers:  List[Customer] = list()

            for customer in customers_left:
                time_for_distance = get_time_between(last_delivery_x, last_delivery_y, customer.x, customer.y)
                time_to_get_back_to_warehouse = get_time_between(vrptw.warehouse.x, vrptw.warehouse.y, customer.x, customer.y)
                estimated_arrival = last_delivery_time + time_for_distance
                if (
                    customer.due_time >= estimated_arrival
                    and customer.demand <= current_truck.package_left
                    and time_to_get_back_to_warehouse + max(last_delivery_time + time_for_distance, customer.ready_time) + customer.service <= vrptw.warehouse.due_time
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
    
    return routes