from math import sqrt
from config import TIME_BY_DISTANCE_UNIT

def distance(x1, y1, x2, y2) -> float:
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def get_time_between(x1, x2, y1, y2) -> float:
    return distance(x1, x2, y1, y2) * TIME_BY_DISTANCE_UNIT

def switch_two_deliveries_in_same_route(route, delivery_one, delivery_two):
    # step 1 : search delivery_one in route
    # step 2 : search delivery_two in route
    # step 3 : reverse
    # step 4 (?) : check if it works for time constraints
    return route