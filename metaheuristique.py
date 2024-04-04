import copy
from model.VRPTW import VRPTW
from utils import fitness, fitness_vrptwless, exchange_route_chunk, switch_two_deliveries_with_routes, reverse, relocate_delivery
from typing import Tuple  
# ALLOWED_OPERATORS = {
#     exchange_route_chunk: [2, 4],
#     switch_two_deliveries: [2],
#     reverse: [1],
#     relocate_delivery: [2, 3],
# }

ALLOWED_OPERATORS = [
    "switch_two_deliveries_with_routes",
]

SIZE_TABU = 10

def tabu_search(vrptw : VRPTW, size_tabu = SIZE_TABU) -> Tuple[VRPTW, int] :
    x_min = vrptw
    f_min = fitness(vrptw)
    tabu = []
    print(f_min)

    previous_x = None
    for _ in range(1000) :
        # print(i)
        current_x, f_current_x, action = get_neighborhood_without_tabu_list(copy.deepcopy(vrptw), tabu)
        # print(current_x, f_current_x, action)
        if previous_x is not None :
            f_previous_x = fitness(previous_x)
            delta_f = f_current_x - f_previous_x
            if delta_f >= 0 :
                tabu.append(action)
                if(len(tabu) > size_tabu):
                    tabu.pop(0)
                print([(action[3], action[4]) for action in tabu])
        if f_current_x < f_min :
            x_min = current_x
            f_min = f_current_x
            print(f_min)
        previous_x = current_x
    return x_min, f_min

def get_neighborhood_without_tabu_list(vrptw : VRPTW, tabu, allowed_operators = ALLOWED_OPERATORS):
    '''
    récupère le voisin avec la meilleur fitness
    '''
    # TODO : copier coller l'attribut routes de VRPTW
    best_f = None
    best_action = None
    best_neighbor = None
    for operator in allowed_operators:
        for _ in range(1000): # TODO : générer tous les voisins
            # print(f"n : {i}")
            match operator:
                # Attention, pour le reverse il faut qu'ils soient dans la même route
                case "switch_two_deliveries_with_routes":
                    r1 = vrptw.get_random_route()
                    d1 = r1.get_random_delivery_index()
                    r2 = vrptw.get_random_route()
                    d2 = r2.get_random_delivery_index()
                    action = ("switch_two_deliveries_with_routes", r1, r2, d1, d2)
                    if action in tabu: # TODO : aussi vérifier dans l'autre sens (inverser routes et clients)
                        # Le tirage est invalide, on continue
                        continue
                    switch_two_deliveries_with_routes(route_one=r1, route_two=r2, delivery_one_index=d1, delivery_two_index=d2, warehouse=vrptw.warehouse)
            f_neigbhor = fitness(vrptw)
            if best_f is None or f_neigbhor < best_f :
                best_neighbor = vrptw
                best_action = action
                best_f = f_neigbhor

    return best_neighbor, best_f, best_action


# function(routes, warehouse, delivery_1, **{random.choice["delivery_next","delivery_previous"]:delivery_2})
# *[]