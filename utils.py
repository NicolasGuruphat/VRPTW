from math import sqrt
from typing import List, Union
from config import TIME_BY_DISTANCE_UNIT, TRUCK_WEIGHT_IN_FITNESS, TRUCK_PACKAGE_LEFT_PER_CENTAGE_IMPACT
from model.Delivery import Delivery
from model.Warehouse import Warehouse
from model.Route import Route
from model.VRPTW import VRPTW

def distance(x1, y1, x2, y2) -> float:
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def get_time_between(x1, x2, y1, y2) -> float:
    return distance(x1, x2, y1, y2) * TIME_BY_DISTANCE_UNIT

def total_distance(route, warehouse):
    d = 0
    if len(route.path) <= 0:
        return d
    
    d += distance(warehouse.x, warehouse.y, route.path[0].customer.x, route.path[0].customer.y)
    for i in range(len(route.path) - 1):
        starting_point = route.path[i].customer
        ending_point = route.path[i+1].customer
        d += distance(starting_point.x, starting_point.y, ending_point.x, ending_point.y)
    d += distance(warehouse.x, warehouse.y, route.path[-1].customer.x, route.path[-1].customer.y)

    return d

def fitness(vrptw : VRPTW) -> float:
    fitness = 0

    for route in vrptw.routes:
        fitness += total_distance(route, vrptw.warehouse) # + TRUCK_WEIGHT_IN_FITNESS + ((route.delivery_truck.package_left) / route.delivery_truck.package_limit * 100 * TRUCK_PACKAGE_LEFT_PER_CENTAGE_IMPACT)
    
    return fitness

def fitness_vrptwless(routes : List[Route], warehouse: Warehouse) -> float:
    fitness = 0

    for route in routes:
        fitness += total_distance(route, warehouse) # + TRUCK_WEIGHT_IN_FITNESS + ((route.delivery_truck.package_left) / route.delivery_truck.package_limit * 100 * TRUCK_PACKAGE_LEFT_PER_CENTAGE_IMPACT)
    
    return fitness

def switch_two_deliveries(routes: List[Route], delivery_one: Delivery, delivery_two: Delivery, warehouse: Warehouse):
    route_one = [route for route in routes if delivery_one in route.path]
    if not route_one:
        return False
    route_two = [route for route in routes if delivery_two in route.path]
    if not route_two:
        return False
    
    if route_one == route_two:
        route_one = route_one[0]
        return switch_two_deliveries_in_same_route(
            route_one, 
            route_one.path.index(delivery_one), 
            route_one.path.index(delivery_two),
            warehouse
        )
    else:
        route_one = route_one[0]
        route_two = route_two[0]
        return switch_two_deliveries_different_route(
            route_one, route_two, 
            route_one.path.index(delivery_one), 
            route_two.path.index(delivery_two), 
            warehouse
        )
    return False

def relocate_delivery(routes: List[Route], delivery_to_relocate: Delivery, warehouse: Warehouse, delivery_new_previous: Union[Delivery, None] = None, delivery_new_next: Union[Delivery, None] = None):
    route_source = [route for route in routes if delivery_to_relocate in route.path]
    if not route_source:
        return False

    route_dest_prev = []
    route_dest_next = []
    if delivery_new_previous:
        route_dest_prev = [route for route in routes if delivery_new_previous in route.path]
    if delivery_new_next:
        route_dest_next = [route for route in routes if delivery_new_next in route.path]

    if (route_dest_prev != route_dest_next and delivery_new_next and delivery_new_previous) or not (route_dest_next or route_dest_prev):
        return False
    
    route_dest = route_dest_prev + [r for r in route_dest_next if r not in route_dest_prev]
    
    if route_source == route_dest:
        route_source = route_source[0]
        return relocate_delivery_in_same_route(
            route_source, 
            route_source.path.index(delivery_to_relocate), 
            warehouse,
            route_source.path.index(delivery_new_previous) if delivery_new_previous else None, 
            route_source.path.index(delivery_new_next) if delivery_new_next else None, 
        )
    else:
        route_source = route_source[0]
        route_dest = (route_dest + route_dest_next)[0]
        return relocate_delivery_different_route(
            route_source, 
            route_dest, 
            route_source.path.index(delivery_to_relocate), 
            warehouse, 
            route_dest.path.index(delivery_new_previous) if delivery_new_previous else None, 
            route_dest.path.index(delivery_new_next) if delivery_new_next else None
        )
    return False
    
def reverse(routes: List[Route], warehouse: Warehouse, delivery_from: Union[Delivery, None] = None, delivery_to: Union[Delivery, None] = None):
    route_from = []
    route_to = []
    if delivery_from:
        route_from = [route for route in routes if delivery_from in route.path]
    if delivery_to:
        route_to = [route for route in routes if delivery_to in route.path]
    
    if (route_from != route_to and route_from and route_to):
        return False
    
    route = route_from + [r for r in route_to if r not in route_from]
    
    index_delivery_from = None
    index_delivery_to = None

    if route:
        route = route[0]
        if delivery_from:
           index_delivery_from = route.path.index(delivery_from) 
        if delivery_to:
           index_delivery_to = route.path.index(delivery_to)

        return reverse_in_same_route(route, warehouse, index_delivery_from, index_delivery_to)
    return False

def exchange_route_chunk(routes: List[Route], warehouse: Warehouse, delivery_from_one: Union[Delivery, None] = None, delivery_to_one: Union[Delivery, None] = None, delivery_from_two: Union[Delivery, None] = None, delivery_to_two: Union[Delivery, None] = None):
    route_one_from = []
    route_one_to = []
    if delivery_from_one:
        route_one_from = [route for route in routes if delivery_from_one in route.path]
    if delivery_to_one:
        route_one_to = [route for route in routes if delivery_to_one in route.path]

    if (route_one_from != route_one_to and delivery_from_one and delivery_to_one) or not (route_one_from or route_one_to):
        return False
    
    route_one = route_one_from + [r for r in route_one_to if r not in route_one_from]

    route_two_from = []
    route_two_to = []
    if delivery_from_two:
        route_two_from = [route for route in routes if delivery_from_two in route.path]
    if delivery_to_two:
        route_two_to = [route for route in routes if delivery_to_two in route.path]

    if (route_two_from != route_two_to and delivery_from_two and delivery_to_two) or not (route_two_from or route_two_to):
        return False
    
    route_two = route_two_from + [r for r in route_two_to if r not in route_two_from]

    if route_one == route_two:
        print("Not implemented yet : exchange_route_chunk_in_same_route")
    else:
        index_from_one = None
        index_to_one = None
        index_from_two = None
        index_to_two = None

        if route_one and route_two:
            if delivery_from_one:
                index_from_one = route_one[0].path.index(delivery_from_one) 
            if delivery_to_one:
                index_to_one = route_one[0].path.index(delivery_to_one) 

            if delivery_from_two:
                index_from_two = route_two[0].path.index(delivery_from_two) 
            if delivery_to_two:
                index_to_two = route_two[0].path.index(delivery_to_two) 

        return exchange_route_chunk_different_route(
            route_one[0], 
            route_two[0], 
            warehouse, 
            index_from_one,
            index_to_one,
            index_from_two,
            index_to_two
        )
    return False

def update_delivery_time_if_possible(params: List) -> bool:
    """Updates if all new routes are working

    Args:
        params (List): list of (deliveries: List[Delivery], beginning_x, beginning_y, beginning_time, warehouse)

    Returns:
        bool: are new time windows working
    """
    global_new_times = list()
    
    for deliveries, beginning_x, beginning_y, beginning_time, warehouse in params:
        new_times = list()

        for delivery in deliveries:
            delivery_time = max(delivery.customer.ready_time, beginning_time + get_time_between(beginning_x, beginning_y, delivery.customer.x, delivery.customer.y))
            # print(f"Deli {delivery.customer.id_name} - {delivery.is_on_time}")

            if not (delivery_time >= delivery.customer.ready_time and delivery_time <= delivery.customer.due_time):
                # print(f"It didn't work 1 !")
                return False
            else:
                new_times.append(delivery_time)
            
            beginning_x = delivery.customer.x
            beginning_y = delivery.customer.y
            beginning_time = delivery_time + delivery.customer.service

        global_new_times.append(new_times)

        if deliveries and get_time_between(deliveries[-1].customer.x, deliveries[-1].customer.y, warehouse.x, warehouse.y) + new_times[-1] > warehouse.due_time:
            # print(f"It didn't work 2 !")
            return False

    for new_times, deliveries in zip(global_new_times, [e[0] for e in params]):
        for new_time, delivery in zip(new_times, deliveries):
            delivery.delivery_time = new_time

    # print(f"It worked !")
    
    return True
    
def switch_two_deliveries_in_same_route(route: Route, index_delivery_one: int, index_delivery_two: int, warehouse: Warehouse):
    # TODO : switch time
    # step 0 (?) : check if it works for time constraints (or it will be done before the call of this function)

    if index_delivery_one == index_delivery_two or max(index_delivery_one, index_delivery_two) >= len(route.path):
        return False

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
        beginning_delivery = route.path[index_min - 1]
        beginning_time = beginning_delivery.departure
        beginning_x = beginning_delivery.customer.x
        beginning_y = beginning_delivery.customer.y

    changed_deliveries = route.path[index_min:]

    changed_deliveries[index_delivery_one - index_min] = delivery_two
    changed_deliveries[index_delivery_two - index_min] = delivery_one

    if not update_delivery_time_if_possible([(changed_deliveries, beginning_x, beginning_y, beginning_time, warehouse)]):
        return False

    # step 3 : reverse
    route.path[index_delivery_one] = delivery_two
    route.path[index_delivery_two] = delivery_one
    
    return True

def switch_two_deliveries_different_route(route_one: Route, route_two: Route, index_delivery_one: int, index_delivery_two: int, warehouse: Warehouse):
    # TODO : switch time
    # step 0 (?) : check if it works for time constraints (or it will be done before the call of this function)

    if index_delivery_one >= len(route_one.path) or index_delivery_two >= len(route_two.path) :
        return False

    # step 1 : search delivery_one in route
    # index_delivery_one = route.path.index(delivery_one)
    delivery_one: Delivery = route_one.path[index_delivery_one]

    # step 2 : search delivery_two in route
    # index_delivery_two = route.path.index(delivery_two)
    delivery_two: Delivery = route_two.path[index_delivery_two]

    if route_one.delivery_truck.package_left + delivery_one.customer.demand - delivery_two.customer.demand < 0 or route_two.delivery_truck.package_left + delivery_two.customer.demand - delivery_one.customer.demand < 0:
        return False

    beginning_time_one = beginning_time_two = 0
    beginning_x_one = beginning_x_two = warehouse.x
    beginning_y_one = beginning_y_two = warehouse.y

    if index_delivery_one > 0:
        beginning_delivery = route_one.path[index_delivery_one - 1]
        beginning_time_one = beginning_delivery.departure
        beginning_x_one = beginning_delivery.customer.x
        beginning_y_one = beginning_delivery.customer.y
    if index_delivery_two > 0:
        beginning_delivery = route_two.path[index_delivery_two - 1]
        beginning_time_two = beginning_delivery.departure
        beginning_x_two = beginning_delivery.customer.x
        beginning_y_two = beginning_delivery.customer.y

    changed_deliveries_one = route_one.path[index_delivery_one:]
    changed_deliveries_two = route_two.path[index_delivery_two:]

    changed_deliveries_one[0] = delivery_two
    changed_deliveries_two[0] = delivery_one
    
    if not update_delivery_time_if_possible(
            [
                (changed_deliveries_one, beginning_x_one, beginning_y_one, beginning_time_one, warehouse), 
                (changed_deliveries_two, beginning_x_two, beginning_y_two, beginning_time_two, warehouse)
            ]
        ):
        return False

    # step 3 : reverse
    route_one.path[index_delivery_one] = delivery_two
    route_two.path[index_delivery_two] = delivery_one
    
    route_one.delivery_truck.package_left += (delivery_one.customer.demand - delivery_two.customer.demand)
    route_two.delivery_truck.package_left += (delivery_two.customer.demand - delivery_one.customer.demand)

    return True

def relocate_delivery_in_same_route(route: Route, index_delivery_to_relocate: int, warehouse: Warehouse, index_delivery_new_previous: Union[int, None] = None, index_delivery_new_next: Union[int, None] = None):
    # TODO : switch time
    # step 0 (?) : check if it works for time constraints (or it will be done before the call of this function)

    if index_delivery_new_next is None and index_delivery_new_previous is not None:
        index_delivery_new_next = index_delivery_new_previous + 1
    elif index_delivery_new_next is not None and index_delivery_new_previous is None:
        index_delivery_new_previous = index_delivery_new_next - 1
    elif (
            (index_delivery_new_previous is None and index_delivery_new_next is None)
            or (index_delivery_new_previous is not None and index_delivery_new_next is not None and index_delivery_new_next != index_delivery_new_previous + 1)
        ):
        return False
        
    if (
            max(
                index_delivery_to_relocate, 
                index_delivery_new_previous
            ) >= len(route.path)
            or min(
                index_delivery_to_relocate, 
                index_delivery_new_next
            ) <= -1
            or index_delivery_to_relocate == index_delivery_new_next or index_delivery_to_relocate == index_delivery_new_previous
        ):
        return False

    # step 1 : search delivery_one in route
    # index_delivery_one = route.path.index(delivery_one)
    delivery_to_relocate = route.path[index_delivery_to_relocate]

    # step 2 : search delivery_two in route
    # index_delivery_two = route.path.index(delivery_two)
    # delivery_two = route.path[index_delivery_two]

    beginning_time = 0
    beginning_x = warehouse.x
    beginning_y = warehouse.y
    index_min = 0

    if index_delivery_new_previous == 0 or (index_delivery_new_previous is not None and index_delivery_new_previous < index_delivery_to_relocate):
        beginning_delivery = route.path[index_delivery_new_previous]
        beginning_time = beginning_delivery.departure
        beginning_x = beginning_delivery.customer.x
        beginning_y = beginning_delivery.customer.y
        index_min = index_delivery_new_previous + 1
    elif ((index_delivery_new_previous is not None and index_delivery_to_relocate < index_delivery_new_previous)
          or
          (index_delivery_new_next is not None and index_delivery_to_relocate < index_delivery_new_next)):
        beginning_delivery = route.path[index_delivery_to_relocate]
        beginning_time = beginning_delivery.departure
        beginning_x = beginning_delivery.customer.x
        beginning_y = beginning_delivery.customer.y
        index_min = index_delivery_to_relocate
    elif index_delivery_new_previous is None and index_delivery_new_next is not None and index_delivery_new_next < index_delivery_to_relocate:
        beginning_delivery = route.path[index_delivery_new_next]
        beginning_time = beginning_delivery.departure
        beginning_x = beginning_delivery.customer.x
        beginning_y = beginning_delivery.customer.y
        index_min = index_delivery_new_next

    changed_deliveries = route.path[index_min:]


    if index_delivery_new_next >= len(route.path):
        changed_deliveries.append(delivery_to_relocate)
        del changed_deliveries[0]
    else:
        changed_deliveries.insert(index_delivery_new_next - index_min, delivery_to_relocate)
        del changed_deliveries[index_delivery_to_relocate - index_min + 1]


    if not update_delivery_time_if_possible([(changed_deliveries, beginning_x, beginning_y, beginning_time, warehouse)]):
        return False

    # step 3 : reverse
    if index_delivery_new_next >= len(route.path):
        route.path.append(delivery_to_relocate)
        del route.path[0]
    else:
        route.path.insert(index_delivery_new_next, delivery_to_relocate)
        del route.path[index_delivery_to_relocate + (1 if index_delivery_new_next < index_delivery_to_relocate else 0)]
    
    return True

def relocate_delivery_different_route(route_source: Route, route_dest: Route, index_delivery_to_relocate: int, warehouse: Warehouse, index_delivery_new_previous: Union[int, None] = None, index_delivery_new_next: Union[int, None] = None):
    # TODO : switch time
    # step 0 (?) : check if it works for time constraints (or it will be done before the call of this function)

    if index_delivery_new_next is None and index_delivery_new_previous is not None:
        index_delivery_new_next = index_delivery_new_previous + 1
    elif index_delivery_new_next is not None and index_delivery_new_previous is None:
        index_delivery_new_previous = index_delivery_new_next - 1
    elif (
            (index_delivery_new_previous is None and index_delivery_new_next is None)
            or (index_delivery_new_previous is not None and index_delivery_new_next is not None and index_delivery_new_next != index_delivery_new_previous + 1)
        ):
        return False
        
    if (
            index_delivery_new_previous >= len(route_dest.path)
            or index_delivery_new_next <= -1
            or index_delivery_to_relocate >= len(route_source.path)
            or index_delivery_to_relocate < 0
        ):
        return False

    # step 1 : search delivery_one in route
    # index_delivery_one = route.path.index(delivery_one)
    delivery_to_relocate = route_source.path[index_delivery_to_relocate]

    if route_dest.delivery_truck.package_left < delivery_to_relocate.customer.demand:
        return False

    # step 2 : search delivery_two in route
    # index_delivery_two = route.path.index(delivery_two)
    # delivery_two = route.path[index_delivery_two]

    beginning_time_source = 0
    beginning_x_source = warehouse.x
    beginning_y_source = warehouse.y

    beginning_time_dest = 0
    beginning_x_dest = warehouse.x
    beginning_y_dest = warehouse.y

    if index_delivery_to_relocate > 0:
        beginning_delivery = route_source.path[index_delivery_to_relocate - 1]
        beginning_time_source = beginning_delivery.delivery_time
        beginning_x_source = beginning_delivery.customer.x
        beginning_y_source = beginning_delivery.customer.y
    
    if index_delivery_new_previous > -1:
        beginning_delivery = route_dest.path[index_delivery_new_previous]
        beginning_time_dest = beginning_delivery.delivery_time
        beginning_x_dest = beginning_delivery.customer.x
        beginning_y_dest = beginning_delivery.customer.y

    changed_deliveries_source = route_source.path[index_delivery_to_relocate + 1:]
    changed_deliveries_dest = [delivery_to_relocate] + route_dest.path[index_delivery_new_next:]

    if not update_delivery_time_if_possible(
            [
                (changed_deliveries_source, beginning_x_source, beginning_y_source, beginning_time_source, warehouse),
                (changed_deliveries_dest, beginning_x_dest, beginning_y_dest, beginning_time_dest, warehouse)
            ]
        ):
        return False

    # step 3 : reverse
    del route_source.path[index_delivery_to_relocate]
    route_dest.path.insert(index_delivery_new_next, delivery_to_relocate)

    route_dest.delivery_truck.package_left -= delivery_to_relocate.customer.demand
    route_source.delivery_truck.package_left += delivery_to_relocate.customer.demand
    
    return True

def reverse_in_same_route(route: Route, warehouse: Warehouse, index_from: Union[int, None] = None, index_to: Union[int, None] = None):
    if index_from is None or index_from < 0:
        index_from = 0
    
    if index_to is None or index_to >= len(route.path):
        index_to = len(route.path) - 1

    if index_to < index_from:
        tmp = index_from
        index_from = index_to
        index_to = tmp

    beginning_time = 0
    beginning_x = warehouse.x
    beginning_y = warehouse.y

    if index_from > 0:
        beginning_delivery = route.path[index_from - 1]
        beginning_time = beginning_delivery.departure
        beginning_x = beginning_delivery.customer.x
        beginning_y = beginning_delivery.customer.y

    reversed_chunk = route.path[index_from:index_to + 1]
    reversed_chunk.reverse()
    changed_deliveries = reversed_chunk + route.path[index_to + 1:]

    if not update_delivery_time_if_possible([(changed_deliveries, beginning_x, beginning_y, beginning_time, warehouse)]):
        return False
    
    route.path = route.path[:index_from] + reversed_chunk + route.path[index_to + 1:]

    return True

def exchange_route_chunk_different_route(route_one: Route, route_two: Route, warehouse: Warehouse, index_from_one: Union[int, None] = None, index_to_one: Union[int, None] = None, index_from_two: Union[int, None] = None, index_to_two: Union[int, None] = None):
    if index_from_one is None or index_from_one < 0:
        index_from_one = 0
    
    if index_to_one is None or index_to_one >= len(route_one.path):
        index_to_one = len(route_one.path) - 1

    if index_from_two is None or index_from_two < 0:
        index_from_two = 0
    
    if index_to_two is None or index_to_two >= len(route_two.path):
        index_to_two = len(route_two.path) - 1

    if index_to_one < index_from_one:
        tmp = index_from_one
        index_from_one = index_to_one
        index_to_one = tmp

    if index_to_two < index_from_two:
        tmp = index_from_two
        index_from_two = index_to_two
        index_to_two = tmp

    package_diff = sum([d.customer.demand for d in route_one.path[index_from_one:index_to_one + 1]]) - sum([d.customer.demand for d in route_two.path[index_from_two:index_to_two + 1]])
    # print(package_diff)
    if route_one.delivery_truck.package_left + package_diff < 0 or route_two.delivery_truck.package_left - package_diff < 0:
        return False

    beginning_time_one = 0
    beginning_x_one = warehouse.x
    beginning_y_one = warehouse.y

    if index_from_one > 0:
        beginning_delivery = route_one.path[index_from_one - 1]
        beginning_time_one = beginning_delivery.departure
        beginning_x_one = beginning_delivery.customer.x
        beginning_y_one = beginning_delivery.customer.y

    beginning_time_two = 0
    beginning_x_two = warehouse.x
    beginning_y_two = warehouse.y

    if index_from_two > 0:
        beginning_delivery = route_two.path[index_from_two - 1]
        beginning_time_two = beginning_delivery.departure
        beginning_x_two = beginning_delivery.customer.x
        beginning_y_two = beginning_delivery.customer.y

    changed_deliveries_one = route_two.path[index_from_two:index_to_two + 1] + route_one.path[index_to_one + 1:]
    changed_deliveries_two = route_one.path[index_from_one:index_to_one + 1] + route_two.path[index_to_one + 1:]

    if not update_delivery_time_if_possible(
            [
                (changed_deliveries_one, beginning_x_one, beginning_y_one, beginning_time_one, warehouse),
                (changed_deliveries_two, beginning_x_two, beginning_y_two, beginning_time_two, warehouse)
            ]
        ):
        return False
    
    route_one_copy = route_one.path.copy()
    route_two_copy = route_two.path.copy()
    route_one.path = route_one_copy[:index_from_one] + route_two_copy[index_from_two:index_to_two + 1] + route_one_copy[index_to_one + 1:]
    route_two.path = route_two_copy[:index_from_two] + route_one_copy[index_from_one:index_to_one + 1] + route_two_copy[index_to_two + 1:]

    route_one.delivery_truck.package_left += package_diff
    route_two.delivery_truck.package_left -= package_diff

    return True


### POUR LE TABU ####################################################################################################################################################################

def switch_two_deliveries_with_routes(route_one: Route, route_two: Route, delivery_one_index: int, delivery_two_index: int, warehouse: Warehouse):
    if not route_one:
        return
    if not route_two:
        return
    
    if route_one == route_two:
        switch_two_deliveries_in_same_route(
            route_one, 
            delivery_one_index, 
            delivery_two_index,
            warehouse
        )
    else:
        switch_two_deliveries_different_route(
            route_one, route_two, 
            delivery_one_index, 
            delivery_two_index, 
            warehouse
        )