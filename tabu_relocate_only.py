import copy
from model.VRPTW import VRPTW
from utils import fitness, fitness_vrptwless, reverse_in_same_route, relocate_delivery, exchange_route_chunk, switch_two_deliveries_with_routes, switch_two_deliveries, reverse, relocate_delivery, switch_two_deliveries_in_same_route
from typing import Tuple
from opt import generate_2opt_couples, generate_3opt_couples
from random_solution import random_solution
from printer.printer import display_vrp
import matplotlib.pyplot as plt

SIZE_TABU = 150
ITERATION_NUMBER = 2000
method_used = {
    "3opt" : 0,
    "2opt" : 0,
    "switch_two_deliveries_with_routes" : 0,
    "reverse_same_route" : 0,
    "relocate" : 0
}
result_false = 0
result_true = 0

def tabu_search(vrptw : VRPTW, size_tabu = SIZE_TABU, iteration_number = ITERATION_NUMBER) -> Tuple[VRPTW, int] :
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
    x = []
    y = []
    colors = []
    not_best = 0
    for i in range(iteration_number) :
        print("\n")
        print(i)
        # print(tabu)
        current_x, f_current_x, rollback = get_neighborhood_without_tabu_list(previous_x, tabu)
        if(current_x == None):
            break
        x.append(i)
        y.append(f_current_x)
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
                # print("on ajoute")
                for element in rollback:
                    # print(element)
                    # if element not in tabu :# Voir s'il faut laisser cette ligne
                    tabu.append(element)
                    if(len(tabu) > size_tabu):
                        tabu.pop(0)
        if f_current_x < f_min :
            # print(f"old best : {f_min} ")
            x_min = current_x
            f_min = f_current_x
            print(f"new best : {f_current_x} ")
            colors.append('green')
            not_best = 0
        else :
            print(f"not best : {f_current_x}")
            colors.append('red')
            not_best += 1
        # if not_best >= SIZE_TABU: # to remove ?
        #     break
            
        
        previous_x = current_x

    # print(f"selected_action {selected_action} unselected_action {unselected_action}")
    print("### PARAMETRES ###")
    print(f"taille tabu : {size_tabu}")
    print(f"nombre d'iteration : {iteration_number}")
    print("### RESULTATS ###")
    print(f"ecart : {initial - f_min}")
    print(f"meilleure fitness : {f_min}")
    print(result_true,result_false)
    # print(method_used)
    plt.scatter(x,y, c=colors, s=1)
    plt.show()
    return x_min, f_min

def get_neighborhood_without_tabu_list(vrptw : VRPTW, tabu):
    global method_used
    global result_false
    global result_true
    best_fitness = None
    best_action = None
    for route_1_index, route_1 in enumerate(vrptw.routes):
            for route_2_index, route_2 in enumerate(vrptw.routes):
                for i in range(len(route_1.path)):
                    for j in range(len(route_2.path)):

                        vrptw_copy = copy.deepcopy(vrptw)
                        delivery_to_relocate = vrptw_copy.routes[route_1_index].path[i]
                        delivery_new_previous = vrptw_copy.routes[route_2_index].path[j]

                        if j+1 == len(vrptw_copy.routes[route_2_index].path):
                             # si l'endoroit où on veux insérer n'a pas de suivant
                            delivery_new_next = None
                            delivery_new_next_id = None

                        else:
                            # si l'endoroit où on veux insérer a un suivant
                            delivery_new_next = vrptw_copy.routes[route_2_index].path[j+1]
                            delivery_new_next_id = delivery_new_next.customer.id_name

                        if i == 0:
                            # si la livraison qu'on veux bouger est la premiere du chemin
                            delivery_to_relocate_previous_id = None
                        else:
                            # si la livraison qu'on veux bouger n'est pas la premiere du chemin
                            delivery_to_relocate_previous_id = vrptw_copy.routes[route_1_index].path[i-1].customer.id_name

                        if i+1 == len(vrptw_copy.routes[route_1_index].path):
                            # si la livraison qu'on veux bouger est la dernière du chemin
                            delivery_to_relocate_next_id = None
                        else :
                            # si la livraison qu'on veux bouger n'est pas la dernière du chemin
                            delivery_to_relocate_next_id = vrptw_copy.routes[route_1_index].path[i+1].customer.id_name

                        if delivery_to_relocate.customer.id_name == delivery_new_previous.customer.id_name or delivery_to_relocate.customer.id_name == delivery_new_next_id:
                            # si la livraison qu'on veux bouger est la même que la destination ou que l'arrivée
                            continue

                        if {"base":delivery_to_relocate.customer.id_name, "previous": delivery_new_previous.customer.id_name} in tabu or {"base":delivery_to_relocate.customer.id_name, "next":delivery_new_next_id} in tabu:
                            # si l'action qu'on veux faire se trouve dans la liste tabu
                            # print(tabu)
                            # print({"base":delivery_to_relocate.customer.id_name, "previous": delivery_new_previous.customer.id_name} in tabu, {"base":delivery_to_relocate.customer.id_name, "next":delivery_new_next_id} in tabu)
                        
                            # print("action canceled : ", delivery_new_previous.customer.id_name ,'->', delivery_to_relocate.customer.id_name,'->', delivery_new_next_id)
                            continue

                        
                        result = relocate_delivery(routes=vrptw_copy.routes, delivery_to_relocate=delivery_to_relocate,warehouse=vrptw_copy.warehouse, delivery_new_previous= delivery_new_previous, delivery_new_next=delivery_new_next)
                        if result == False :
                            continue
                        current_fitness = fitness(vrptw_copy)
                        
                        if(best_fitness == None or current_fitness < best_fitness):
                            # print("better for now :", current_fitness)
                            best_fitness = current_fitness
                            best_solution = vrptw_copy
                            best_action =  f'{delivery_new_previous.customer.id_name} -> {delivery_to_relocate.customer.id_name} -> {delivery_new_next_id}' 
                            how_to_rollback = [{"base":delivery_to_relocate.customer.id_name, "previous":delivery_to_relocate_previous_id},{"base":delivery_to_relocate.customer.id_name, "next":delivery_to_relocate_next_id}]
    if(best_action == None):
        return None, None, None
    print("best action : ",best_action)
    return best_solution, best_fitness, how_to_rollback

vrptw = VRPTW('data101_short.vrp')
vrptw.routes = random_solution(vrptw)
tabu =tabu_search(vrptw) 
print(tabu[1])
vrptw = tabu[0]
display_vrp(vrptw.warehouse,vrptw.customers,vrptw.routes, False, False)
display_vrp(vrptw.warehouse, vrptw.customers, vrptw.routes, False, False)