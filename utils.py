from math import sqrt
from config import TIME_BY_DISTANCE_UNIT

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

def switch_two_deliveries_in_same_route(route, delivery_one, delivery_two):
    # TODO : switch time
    # step 0 (?) : check if it works for time constraints (or it will be done before the call of this function)

    # step 1 : search delivery_one in route
    index_delivery_one = route.path.index(delivery_one)

    # step 2 : search delivery_two in route
    index_delivery_two = route.path.index(delivery_two)

    # step 3 : reverse
    route.path[index_delivery_one] = delivery_two
    route.path[index_delivery_two] = delivery_one
    
    return route