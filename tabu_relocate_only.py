import copy
from model.VRPTW import VRPTW
from utils import fitness, fitness_vrptwless, reverse_in_same_route, relocate_delivery, exchange_route_chunk, switch_two_deliveries_with_routes, switch_two_deliveries, reverse, relocate_delivery, switch_two_deliveries_in_same_route
from typing import Tuple
from opt import generate_2opt_couples, generate_3opt_couples
from random_solution import random_solution
from printer.printer import display_vrp

SIZE_TABU = 30

method_used = {
    "3opt" : 0,
    "2opt" : 0,
    "switch_two_deliveries_with_routes" : 0,
    "reverse_same_route" : 0,
    "relocate" : 0
}
result_false = 0
result_true = 0

def tabu_search(vrptw : VRPTW, size_tabu = SIZE_TABU) -> Tuple[VRPTW, int] :
    global selected_action
    global unselected_action
    global result_true
    global result_false
    x_min = vrptw
    f_min = fitness(vrptw)
    tabu = []
    print(f"initial : {f_min}")
    initial = f_min
    previous_x = vrptw
    for i in range(1000) :
        # print(tabu)
        print(i)
        current_x, f_current_x, action = get_neighborhood_without_tabu_list(previous_x, tabu)
        routes_copy = vrptw.routes.copy()
        for route in vrptw.routes:
            if len(route.path) == 0:
                print("EMPTY")
                routes_copy.remove(route)
        vrptw.routes = routes_copy
        if current_x is None or f_current_x is None:
            break
        if previous_x is not None :
            f_previous_x = fitness(previous_x)
            delta_f = f_current_x - f_previous_x
            if delta_f >= 0 :
                for element in action:
                    tabu.append(element)
                    if(len(tabu) > size_tabu):
                        tabu.pop(0)
        if f_current_x < f_min :
            # print(f"old best : {f_min} ")
            x_min = current_x
            f_min = f_current_x
            print(f"new best : {f_min} ")
        else :
            print(f"not best : {f_current_x}")
        previous_x = current_x

    # print(f"selected_action {selected_action} unselected_action {unselected_action}")
    print(f"ecart : {initial - f_min}")
    print(f"meilleure fitness : {f_min}")
    print(result_true,result_false)
    # print(method_used)
    return x_min, f_min

def get_neighborhood_without_tabu_list(vrptw : VRPTW, tabu):
    global method_used
    global result_false
    global result_true
    best_fitness = None

    for route_1_index, route_1 in enumerate(vrptw.routes):
            for route_2_index, route_2 in enumerate(vrptw.routes):
                for i in range(len(route_1.path)):
                    for j in range(len(route_2.path)):
                        vrptw_copy = copy.deepcopy(vrptw)
                        delivery_to_relocate = vrptw_copy.routes[route_1_index].path[i]
                        delivery_new_previous = vrptw_copy.routes[route_2_index].path[j]

                        if j+1 == len(vrptw_copy.routes[route_2_index].path):

                            delivery_new_next = None
                            # print(delivery1.customer.id_name, delivery2.customer.id_name, 'None' )
                        else:
                            delivery_new_next = vrptw_copy.routes[route_2_index].path[j+1]
                            # print(delivery1.customer.id_name, delivery2.customer.id_name, delivery3.customer.id_name )

                        if(delivery_new_next == None):
                            third_parameter = None
                        else:
                            third_parameter = delivery_new_next.customer.id_name

                        # if {"base":third_parameter, "previous":delivery_to_relocate.customer.id_name} in tabu or {"base":delivery_new_next, "next":delivery_to_relocate.customer.id_name} in tabu:
                        #     # print("here2")
                        #     continue

                        # print("fitness before :", fitness(vrptw_copy))
                        # fb = fitness(vrptw_copy)
                        result = relocate_delivery(routes=vrptw_copy.routes, delivery_to_relocate=delivery_to_relocate,warehouse=vrptw_copy.warehouse, delivery_new_previous= delivery_new_previous, delivery_new_next=delivery_new_next)
                        if result:
                            result_true += 1
                        else:
                            result_false += 1
                        # print("fitness after :", fitness(vrptw_copy))
                        # fa = fitness(vrptw_copy)

                        # if(fa-fb != 0):
                            # print('not the same')
                        current_fitness = fitness(vrptw_copy)
                        
                        if(best_fitness == None or current_fitness < best_fitness):
                            # print("better")
                            best_fitness = current_fitness
                            best_solution = vrptw_copy
                            best_action = [{"base":delivery_to_relocate.customer.id_name, "previous":delivery_new_previous.customer.id_name},{"base":delivery_to_relocate.customer.id_name, "next":third_parameter}]
    return best_solution, best_fitness, best_action

vrptw = VRPTW('data101_short.vrp')
vrptw.routes = random_solution(vrptw)
display_vrp(vrptw.warehouse,vrptw.customers,vrptw.routes, False, False)
tabu =tabu_search(vrptw) 
print(tabu[1])
vrptw = tabu[0]
display_vrp(vrptw.warehouse, vrptw.customers, vrptw.routes, False, False)