from copy import deepcopy
from utils import  switch_two_deliveries, fitness, relocate_delivery, reverse, exchange_route_chunk
from model.VRPTW import VRPTW
from random_solution import random_solution
from printer.printer import display_vrp

'''
def hill_climbing(vrptw, best_fitness):
    # best_fitness = 
    # best_solution = 
    operators = [relocate_delivery, switch_two_deliveries, reverse, exchange_route_chunk]
    for route_1_index, route_1 in enumerate(vrptw.routes):
        for route_2_index, route_2 in enumerate(vrptw.routes):
            for i in range(len(route_1.path)):
                for j in range(len(route_2.path)):
                    for operator in operators:
                        vrptw_copy = deepcopy(vrptw)
                        delivery1 = vrptw_copy.routes[route_1_index].path[i]
                        delivery2 = vrptw_copy.routes[route_2_index].path[j]
                        # print(f"{delivery1.customer.id_name,delivery2.customer.id_name, operator}")
                        operator(vrptw_copy.routes, vrptw_copy.warehouse, delivery1, delivery2)
                        current_fitness = fitness(vrptw_copy)
                        if(best_fitness == None or current_fitness < best_fitness):
                            print(current_fitness, best_fitness)
                            return vrptw_copy, current_fitness
                            best_fitness = current_fitness
                            best_solution = vrptw_copy
                            print(f"new best solution : {best_fitness}")
                        
    return vrptw, best_fitness
'''
def hill_climbing_2(vrptw, best_fitness):
    best_solution = None
    operators = [relocate_delivery, switch_two_deliveries]#,reverse, exchange_route_chunk]
    for route_1_index, route_1 in enumerate(vrptw.routes):
        for route_2_index, route_2 in enumerate(vrptw.routes):
            for i in range(len(route_1.path)):
                for j in range(len(route_2.path)):
                    for operator in operators:
                        vrptw_copy = deepcopy(vrptw)
                        delivery1 = vrptw_copy.routes[route_1_index].path[i]
                        delivery2 = vrptw_copy.routes[route_2_index].path[j]
                        operator(vrptw_copy.routes, vrptw_copy.warehouse, delivery1, delivery2)
                        current_fitness = fitness(vrptw_copy)
                        if(best_fitness == None or current_fitness < best_fitness):
                            best_fitness = current_fitness
                            best_solution = vrptw_copy
    return best_solution if best_solution != None else vrptw, best_fitness
'''
def tabu(vrptw):
    best_fitness = 
    best_solution = 
    operators = [relocate_delivery, switch_two_deliveries, reverse, exchange_route_chunk]
    tabu_list = []
    SIZE_TABU = 10
    for route_1_index, route_1 in enumerate(vrptw.routes):
        for route_2_index, route_2 in enumerate(vrptw.routes):
            for i in range(len(route_1.path)):
                for j in range(len(route_2.path)):
                    for operator in operators:
                        vrptw_copy = deepcopy(vrptw)
                        delivery1 = vrptw_copy.routes[route_1_index].path[i]
                        delivery2 = vrptw_copy.routes[route_2_index].path[j]
                        # print(f"{delivery1.customer.id_name,delivery2.customer.id_name, operator}")
                        operator(vrptw_copy.routes, vrptw_copy.warehouse, delivery1, delivery2)
                        current_fitness = fitness(vrptw_copy)
                        if(best_fitness ==  or current_fitness < best_fitness):
                            best_fitness = current_fitness
                            best_solution = vrptw_copy
                            current_solution = vrptw
                            print(f"new best solution : {best_fitness}")
                        else:
                            in_tabu_list = (operator, route_1, route_2, delivery1, delivery2) in tabu_list
                            if not in_tabu_list:
                                tabu_list.append((operator, route_1, route_2, delivery1, delivery2))
                                if(len(tabu_list) > SIZE_TABU):
                                    tabu_list.pop(0)
                                current_solution = vrptw 
    return best_solution, best_fitness
'''

vrptw = VRPTW('data101_short.vrp')
vrptw.routes = random_solution(vrptw)
initial_fitness = fitness(vrptw)
display_vrp(vrptw.warehouse,vrptw.customers,vrptw.routes, False, False)

best = fitness(vrptw)

for i in range(1000):
    print(i)
    old_best = best
    s = hill_climbing_2(vrptw, best)
    vrptw = s[0]
    best = s[1]
    print(best)
    if old_best == best:
        print("here")
        break
display_vrp(vrptw.warehouse, vrptw.customers, vrptw.routes, False, False)
print(f"meilleure solution : {best}, ecart : {initial_fitness - best}")