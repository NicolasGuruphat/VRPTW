from math import sqrt
from typing import List
from config import TIME_BY_DISTANCE_UNIT
from model.Delivery import Delivery
from model.Warehouse import Warehouse
from model.Route import Route

def distance(x1, y1, x2, y2) -> float:
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def get_time_between(x1, x2, y1, y2) -> float:
    return distance(x1, x2, y1, y2) * TIME_BY_DISTANCE_UNIT

def total_distance(route):
    d = 0
    for i in range(len(route.path) - 1):
        starting_point = route.path[i].customer
        ending_point = route.path[i+1].customer
        d += distance(starting_point.x, starting_point.y, ending_point.x, ending_point.y)
    return d

def switch_two_deliveries(routes: List[Route], delivery_one: Delivery, delivery_two: Delivery, warehouse: Warehouse):
    route_one = [route for route in routes if delivery_one in route.path]
    if not route_one:
        return
    route_two = [route for route in routes if delivery_two in route.path]
    if not route_two:
        return
    
    if route_one == route_two:
        route_one = route_one[0]
        switch_two_deliveries_in_same_route(route_one, route_one.path.index(delivery_one), route_one.path.index(delivery_two), warehouse)
    else:
        raise NotImplemented("TO DO ;)")
    

def switch_two_deliveries_in_same_route(route: Route, index_delivery_one: Delivery, index_delivery_two: Delivery, warehouse: Warehouse):
    # TODO : switch time
    # step 0 (?) : check if it works for time constraints (or it will be done before the call of this function)

    if index_delivery_one == index_delivery_two or max(index_delivery_one, index_delivery_two) >= len(route.path):
        return route

    # step 1 : search delivery_one in route
    # index_delivery_one = route.path.index(delivery_one)
    delivery_one = route.path[index_delivery_one]

    # step 2 : search delivery_two in route
    # index_delivery_two = route.path.index(delivery_two)
    delivery_two = route.path[index_delivery_two]

    beginning_time = 0
    beginning_x = warehouse.x
    beginning_y = warehouse.y
    index_min = 0

    if (index_min := min(index_delivery_one, index_delivery_two)) > 0:
        beginning_delivery = route.path[index_min]
        beginning_time = beginning_delivery.departure
        beginning_x = beginning_delivery.customer.x
        beginning_y = beginning_delivery.customer.y

    changed_deliveries = route.path[index_min:]

    changed_deliveries[index_delivery_one - index_min] = delivery_two
    changed_deliveries[index_delivery_two - index_min] = delivery_one
    
    for delivery in changed_deliveries:
        delivery.delivery_time = max(delivery.customer.ready_time, beginning_time + get_time_between(beginning_x, beginning_y, delivery.customer.x, delivery.customer.y))
        print(f"Deli {delivery.customer.id_name} - {delivery.is_on_time}")
        if not delivery.is_on_time:
            return route

    # step 3 : reverse
    route.path[index_delivery_one] = delivery_two
    route.path[index_delivery_two] = delivery_one
    
    return route