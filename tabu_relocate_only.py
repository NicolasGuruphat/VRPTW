import copy
from model.VRPTW import VRPTW
from utils import fitness, fitness_vrptwless, reverse_in_same_route, relocate_delivery, exchange_route_chunk, switch_two_deliveries_with_routes, switch_two_deliveries, reverse, relocate_delivery, switch_two_deliveries_in_same_route
from typing import Tuple
from opt import generate_2opt_couples, generate_3opt_couples
from random_solution import random_solution
from printer.printer import display_vrp
import matplotlib.pyplot as plt
import csv
import time

SIZE_TABU = 20
ITERATION_NUMBER = 200

result_false = 0
result_true = 0

def tabu_search(vrptw : VRPTW, size_tabu = SIZE_TABU, iteration_number = ITERATION_NUMBER, sch_detect = True) -> Tuple[VRPTW, int] :
    global selected_action
    global unselected_action
    global result_true
    global result_false
    print("\n\n\n")
    method_used = {
    # "3opt" : 0,
    "2opt" : 0,
    # "switch_two_deliveries_with_routes" : 0,
    # "reverse_same_route" : 0,
    "relocate" : 0
}
    x_min = vrptw
    f_min = fitness(vrptw)
    tabu = []
    # print(f"initial : {f_min}")
    previous_x = vrptw
    x = []
    y = []
    size = []
    colors = []
    not_best = 0
    # last_fitnesses = []
    # check_pattern = 0
    already_explored = {}
    detected = False
    j = 0
    for i in range(iteration_number) :
        
        current_x, f_current_x, rollback = get_neighborhood_without_tabu_list(previous_x, tabu)
        # print(tabu)
        # if i%10 == 0:
            # print(i)
        # print(i) 
           
        '''
        print("\n")
        print(i)
        print(f"action : {rollback[0][0]}")
        '''
        if(current_x == None or rollback == None):
            print("pas de solution a proposer")
            break
        action = rollback[0][0]
        if action == 'relocate':
            color = "red"
        elif action == '2opt':
            color = "green"
        else:
            color = "black"
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
        
        '''
        last_fitnesses.append(f_current_x)
        if len(last_fitnesses) > size_tabu + 1:
            last_fitnesses.pop(0)
            
        '''
        x.append(i)
        y.append(f_current_x)
        colors.append(color)

        routes_copy = vrptw.routes.copy()
        vrptw.routes = routes_copy
        if current_x is None or f_current_x is None:
            break
        if previous_x is not None :
            f_previous_x = fitness(previous_x)
            delta_f = f_current_x - f_previous_x
            # print(delta_f)
            if delta_f >= 0 and rollback != None:
                # print("on ajoute")
                for element in rollback:
                    # if element not in tabu :# Voir s'il faut laisser cette ligne
                    tabu.append(element)
                    if(len(tabu) > size_tabu):
                        tabu.pop(0)
        if f_current_x < f_min :
            # print(f"old best : {f_min} ")
            x_min = current_x
            f_min = f_current_x
            # print(f"new best : {f_current_x} ")
            # colors.append('green')
            size.append(7)
            not_best = 0
            already_explored = {} # on reset la liste car on est sûr de ne pas être dans un cycle
        else :
            # print(f"not best : {f_current_x}")
            # colors.append('red')
            size.append(1)
            not_best += 1
        # if not_best >= SIZE_TABU: # to remove ?
        #     break
        hash = current_x.str_hash()
        if sch_detect and (current_x.str_hash(), str(tabu)) in already_explored.items():
            if not detected:
                # print("boucle détectée")
                # colors.pop()
                # colors.append('blue')
                color = 'blue'
                break
            detected = True
            # break
            # essayer sans le break pour voir si c'est bien au bon moment qu'on casse la boucle
        if(len(tabu) == size_tabu):
            already_explored[hash] = str(tabu)

        if(len(already_explored) > size_tabu):
            del already_explored[next(iter(already_explored))]
       
        for key, value in already_explored.items():
            print("\n")
            print(key, value)
        # print(tabu)
        previous_x = current_x

        method_used[rollback[0][0]] += 1
        j += 1

    # print(f"selected_action {selected_action} unselected_action {unselected_action}")
    '''
    print(f"nombre d'itération économisées : {iteration_number - j}")
    print("### PARAMETRES ###")
    print(f"taille tabu : {size_tabu}")
    print(f"nombre d'iteration : {iteration_number}")
    print("### RESULTATS ###")
    print(f"nombre d'itération réel : {j}")
    print(f"ecart : {initial - f_min}")
    print(f"meilleure fitness : {f_min}")
    print(method_used)
    print(result_true,result_false)
    # print(method_used)
    plt.scatter(x,y, c=colors, s=size)
    plt.show()
    '''
    return x_min, f_min, j, method_used

def get_neighborhood_without_tabu_list(vrptw : VRPTW, tabu):

    operators = [
        get_neighborhood_without_tabu_list_opt2, 
        get_neighborhood_without_tabu_list_relocate
    ]
    
    best_solution = None
    best_fitness = None
    best_rollback = None

    for operator in operators:
        solution, f, how_to_rollback = operator(copy.deepcopy(vrptw), copy.deepcopy(tabu))
        if f != None and (best_fitness == None or f < best_fitness):
            best_fitness = f
            best_rollback = how_to_rollback
            best_solution = solution
    if solution == None or f == None or how_to_rollback == None:
        return None, None, None
    
    return best_solution, best_fitness, best_rollback


def get_neighborhood_without_tabu_list_relocate(vrptw : VRPTW, tabu):
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

                        if ("relocate",{"base":delivery_to_relocate.customer.id_name, "previous": delivery_new_previous_id}) in tabu or ("relocate",{"base":delivery_to_relocate.customer.id_name, "next":delivery_new_next_id}) in tabu or ("relocate",{"base":delivery_new_previous_id, "next": delivery_to_relocate.customer.id_name}) in tabu or ("relocate",{"base":delivery_new_next_id, "previous": delivery_to_relocate.customer.id_name}) in tabu:
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
                            how_to_rollback = [("relocate",{"base":delivery_to_relocate.customer.id_name, "previous":delivery_to_relocate_previous_id}),("relocate",{"base":delivery_to_relocate.customer.id_name, "next":delivery_to_relocate_next_id})]
    if(best_action == None):
        return None, None, None
    # print("best action : ",best_action)
    # print(vf"best relocate : {best_fitness}")

    return best_solution, best_fitness, how_to_rollback

def get_neighborhood_without_tabu_list_opt2(vrptw : VRPTW, tabu):
    '''
    récupère le voisin avec la meilleur fitness
    '''
 
    # Faire une deep copy de routes avant de la modifier
    best_f = None
    best_action = None
    best_neighbor = None
    best_routes = None
    vrptw_copy = vrptw # TODO : to remove # copy.deepcopy(vrptw)
    for couple in generate_2opt_couples(vrptw_copy.routes):
        route_index = couple[2]
        action = [("2opt", route_index, couple[0], couple[1])]
        if ("2opt", route_index, couple[1], couple[0]) in tabu or ("2opt", route_index, couple[0], couple[1]) in tabu: # voir lequel garder
            # Le tirage est invalide, on saute cette itération
            continue
        
        routes_copy = copy.deepcopy(vrptw_copy.routes)
        result = switch_two_deliveries_in_same_route(routes_copy[route_index], couple[0], couple[1], vrptw_copy.warehouse)  
        if result == False:
            continue
        # vrptw_copy_copy = copy.deepcopy(vrptw_copy)
        # vrptw_copy_copy.routes = routes_copy

        f_neigbhor = fitness_vrptwless(routes_copy, vrptw_copy.warehouse)

        if best_f is None or f_neigbhor < best_f :
            
            best_routes = routes_copy 
            best_action = action
            best_f = f_neigbhor
    # print(best_f)
    if(best_routes == None):
        return None, None, None
    best_neighbor = vrptw_copy
    best_neighbor.routes = best_routes
    # print(f"best 2 opt : {best_f}")
    return best_neighbor, best_f, best_action


SAME_PARAMETERS = 2
file_name = "./tabu_relocate_only/test_101_short.csv"
with open(file_name, "w", newline="") as file:
    csv.writer(file).writerow(["size_tabu", "nb_iteration", "avg_fitness", "min_fitness", "max_fitness", "avg_iteration", "min_iteration", "max_iteration", "avg_duration", "min_duration", "max_duration", "avg_relocate (%)", "avg_2_opt (%)"])

size_tabu_list = [0,4,16,64]
nb_iteration_list = [0, 40, 160, 640]
# todo : uncomment above

# size_tabu_list = [0,4]
# nb_iteration_list = [10,20]
 
# file_list = ["data101_short.vrp"]
# for file in file_list
for size_tabu in size_tabu_list:
    for nb_iteration in nb_iteration_list:
        print(f"\nstart size_tabu : {size_tabu}, nb_iteration {nb_iteration}\n")
        
        sum_fitness = 0
        min_fitness = None
        max_fitness = None

        sum_iteration = 0
        min_iteration = None
        max_iteration = None

        sum_relocate = 0
        sum_2_opt = 0

        sum_duration = 0
        min_duration = None
        max_duration = None
        for i in range(SAME_PARAMETERS):
            vrptw = VRPTW('data101_short.vrp')
            vrptw.routes = random_solution(vrptw)
            cp_routes = copy.deepcopy(vrptw.routes)
            begin = time.time()
            s,f,j, method_used = tabu_search(vrptw, size_tabu, nb_iteration, False)
            duration = time.time() - begin
            sum_fitness += f
            sum_iteration += j
            sum_duration += duration
            sum_relocate += method_used['relocate']
            sum_2_opt += method_used['2opt']

            if min_duration == None or duration < min_duration:
                min_duration = duration
            if max_duration == None or duration > max_duration:
                max_duration = duration

            if min_fitness == None or f < min_fitness:
                min_fitness = f
            if max_fitness == None or f > max_fitness:
                max_fitness = f
            
            if min_iteration == None or j < min_iteration:
                min_iteration = j
            if max_iteration == None or j > max_iteration:
                max_iteration = j
             
        avg_fitness = sum_fitness/SAME_PARAMETERS
        avg_iteration = sum_iteration/SAME_PARAMETERS
        avg_duration = sum_duration/SAME_PARAMETERS
        
        avg_relocate_percentage = 0
        avg_2_opt_percentage = 0

        total_action = sum_relocate + sum_2_opt
        if total_action != 0:
            avg_relocate = sum_relocate/SAME_PARAMETERS#/total_action*100
            avg_2_opt = sum_2_opt/SAME_PARAMETERS#/total_action*100
            total = avg_relocate + avg_2_opt
            
            avg_relocate_percentage = round(avg_relocate / total * 100,4)
            avg_2_opt_percentage = round(avg_2_opt / total * 100,4)

        with open(file_name, "a", newline="") as file:
            csv.writer(file).writerow([size_tabu, nb_iteration, avg_fitness, min_fitness, max_fitness, avg_iteration, min_iteration, max_iteration, avg_duration, min_duration, max_duration, avg_relocate_percentage, avg_2_opt_percentage])

'''
vrptw = VRPTW('data101_short.vrp')
vrptw.routes = random_solution(vrptw)
# display_vrp(vrptw.warehouse,vrptw.customers,vrptw.routes, False, False)
tabu =tabu_search(vrptw) 
print(tabu[1])
vrptw = tabu[0]
display_vrp(vrptw.warehouse, vrptw.customers, vrptw.routes, False, False)
'''