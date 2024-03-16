from math import sqrt
from config import TIME_BY_DISTANCE_UNIT

def distance(x1, y1, x2, y2) -> float:
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def get_time_between(x1, x2, y1, y2) -> float:
    return distance(x1, x2, y1, y2) * TIME_BY_DISTANCE_UNIT