import copy
from model.VRPTW import VRPTW
from utils import fitness, fitness_vrptwless, reverse_in_same_route, relocate_delivery, exchange_route_chunk, switch_two_deliveries_with_routes, switch_two_deliveries, reverse, relocate_delivery, switch_two_deliveries_in_same_route
from typing import Tuple
from opt import generate_2opt_couples, generate_3opt_couples
from random_solution import random_solution
from printer.printer import display_vrp
import matplotlib.pyplot as plt
import csv

SIZE_TABU = 30
ITERATION_NUMBER = 1000
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
    # print(f"initial : {f_min}")
    initial = f_min
    previous_x = vrptw
    x = []
    y = []
    colors = []
    not_best = 0
    # last_fitnesses = []
    # check_pattern = 0
    already_explored = {}
    detected = False
    for i in range(iteration_number) :
        print("\n")
        print(i)
        current_x, f_current_x, rollback = get_neighborhood_without_tabu_list(previous_x, tabu)
        ''' 
        if len(last_fitnesses) != 0 and f_current_x == last_fitnesses[0]:
            check_pattern += 1
            print(f"check pattern : {check_pattern}")
        else :
            check_pattern = 0
        if check_pattern == size_tabu:
            print("pattern detecté")
            break
        '''
        if(current_x == None):
            print("pas de solution a proposer")
            break
        '''
        last_fitnesses.append(f_current_x)
        if len(last_fitnesses) > size_tabu + 1:
            last_fitnesses.pop(0)
            
        '''
        x.append(i)
        y.append(f_current_x)
        routes_copy = vrptw.routes.copy()
        vrptw.routes = routes_copy
        if current_x is None or f_current_x is None:
            break
        if previous_x is not None :
            f_previous_x = fitness(previous_x)
            delta_f = f_current_x - f_previous_x
            if delta_f >= 0 and rollback != None:
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
            already_explored = {} # on reset la liste car on est sûr de ne pas être dans un cycle
        else :
            print(f"not best : {f_current_x}")
            colors.append('red')
            not_best += 1
        # if not_best >= SIZE_TABU: # to remove ?
        #     break
        if (str(f_current_x), str(tabu)) in already_explored.items():
            if not detected:
                print("boucle détectée")
                colors.pop()
                colors.append('blue')
                break
            detected = True
            # break
            # essayer sans le break pour voir si c'est bien au bon moment qu'on casse la boucle
        if(len(tabu) == size_tabu):
            already_explored[str(f_current_x)] = str(tabu)
        
        # print(tabu)
        previous_x = current_x

    
    # print(f"selected_action {selected_action} unselected_action {unselected_action}")
    print("### PARAMETRES ###")
    print(f"taille tabu : {size_tabu}")
    print(f"nombre d'iteration : {iteration_number}")
    print("### RESULTATS ###")
    print(f"nombre d'itération réel : {i}")
    print(f"nombre d'itération économisées : {iteration_number - i}")
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
                    for j in range(-1,len(route_2.path)):
                        vrptw_copy = copy.deepcopy(vrptw)

                        if(j == -1):
                            # si on veux déplacer en première position
                            delivery_new_previous = None
                            delivery_new_previous_id = None
                        else:
                            delivery_new_previous = vrptw_copy.routes[route_2_index].path[j]
                            delivery_new_previous_id = delivery_new_previous.customer.id_name

                        delivery_to_relocate = vrptw_copy.routes[route_1_index].path[i]

                        if j+1 == len(vrptw_copy.routes[route_2_index].path):
                             # si l'endoroit où on veux insérer n'a pas de suivant
                            delivery_new_next = None
                            delivery_new_next_id = None
                            # continue # test en enlevant les none

                        else:
                            # si l'endoroit où on veux insérer a un suivant
                            delivery_new_next = vrptw_copy.routes[route_2_index].path[j+1]
                            delivery_new_next_id = delivery_new_next.customer.id_name

                        if i == 0:
                            # si la livraison qu'on veux bouger est la premiere du chemin
                            delivery_to_relocate_previous_id = None
                            # continue # test en enlevant les none
                        else:
                            # si la livraison qu'on veux bouger n'est pas la premiere du chemin
                            delivery_to_relocate_previous_id = vrptw_copy.routes[route_1_index].path[i-1].customer.id_name

                        if i+1 == len(vrptw_copy.routes[route_1_index].path):
                            # si la livraison qu'on veux bouger est la dernière du chemin
                            delivery_to_relocate_next_id = None
                            # continue # test en enlevant les none
                        else :
                            # si la livraison qu'on veux bouger n'est pas la dernière du chemin
                            delivery_to_relocate_next_id = vrptw_copy.routes[route_1_index].path[i+1].customer.id_name

                        if delivery_to_relocate.customer.id_name == delivery_new_previous_id or delivery_to_relocate.customer.id_name == delivery_new_next_id:
                            # si la livraison qu'on veux bouger est la même que la destination ou que l'arrivée
                            continue

                        if {"base":delivery_to_relocate.customer.id_name, "previous": delivery_new_previous_id} in tabu or {"base":delivery_to_relocate.customer.id_name, "next":delivery_new_next_id} in tabu or {"base":delivery_new_previous_id, "next": delivery_to_relocate.customer.id_name} in tabu or {"base":delivery_new_next_id, "previous": delivery_to_relocate.customer.id_name} in tabu:
                            # si l'action qu'on veux faire se trouve dans la liste tabu
                            # print(tabu)
                            # print({"base":delivery_to_relocate.customer.id_name, "previous": delivery_new_previous.customer.id_name} in tabu, {"base":delivery_to_relocate.customer.id_name, "next":delivery_new_next_id} in tabu)
                        
                            # print("action canceled : ", delivery_new_previous.customer.id_name ,'->', delivery_to_relocate.customer.id_name,'->', delivery_new_next_id)
                            continue

                        fitness_before = fitness(vrptw_copy)
                        result = relocate_delivery(routes=vrptw_copy.routes, delivery_to_relocate=delivery_to_relocate,warehouse=vrptw_copy.warehouse, delivery_new_previous= delivery_new_previous, delivery_new_next=delivery_new_next)
                        
                        

                        if result == False :
                            # Si l'action n'a pas pu être réalisée
                            continue

                        for route in vrptw_copy.routes:
                            if len(route.path) == 0:
                                # print("empty")
                                vrptw_copy.routes.remove(route)

                        current_fitness = fitness(vrptw_copy)
                        
                        if(current_fitness == fitness_before):
                            # gestion du bug de l'action qui n'est pas prise en compte
                            continue
                        
                        if(best_fitness == None or current_fitness < best_fitness):
                            # print("better for now :", current_fitness)
                            best_fitness = current_fitness
                            best_solution = vrptw_copy
                            best_action =  f'{delivery_new_previous_id} -> {delivery_to_relocate.customer.id_name} -> {delivery_new_next_id}' 
                            how_to_rollback = [{"base":delivery_to_relocate.customer.id_name, "previous":delivery_to_relocate_previous_id},{"base":delivery_to_relocate.customer.id_name, "next":delivery_to_relocate_next_id}]
    if(best_action == None):
        return None, None, None
    print("best action : ",best_action)
    return best_solution, best_fitness, how_to_rollback
'''
SAME_PARAMETERS = 2

with open(f"./tabu_relocate_only/sim_2.csv", "w", newline="") as file:
    csv.writer(file).writerow(["size_tabu", "nb_iteration", "avg"])

for size_tabu in range(0,200, 2):
    for nb_iteration in range(0, 2000, 100):
        print(f"start {size_tabu} {nb_iteration}")
        sum = 0
        for i in range(SAME_PARAMETERS):
            vrptw = VRPTW('data101_short.vrp')
            vrptw.routes = random_solution(vrptw)
            tabu = tabu_search(vrptw, size_tabu, nb_iteration)
            sum += tabu[1]
        avg = sum/SAME_PARAMETERS
        with open(f"./tabu_relocate_only/sim_2.csv", "a", newline="") as file:
            csv.writer(file).writerow([size_tabu, nb_iteration, avg])
'''
vrptw = VRPTW('data101_short.vrp')
vrptw.routes = random_solution(vrptw)
# display_vrp(vrptw.warehouse,vrptw.customers,vrptw.routes, False, False)
tabu =tabu_search(vrptw) 
print(tabu[1])
vrptw = tabu[0]
display_vrp(vrptw.warehouse, vrptw.customers, vrptw.routes, False, False)