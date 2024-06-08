import copy
from model.VRPTW import VRPTW
from utils import fitness, fitness_vrptwless, reverse_in_same_route, relocate_delivery, exchange_route_chunk, switch_two_deliveries_with_routes, switch_two_deliveries, reverse, relocate_delivery, switch_two_deliveries_in_same_route
from typing import Tuple
from opt import generate_2opt_couples, generate_3opt_couples

SIZE_TABU = 10 

method_used = {
    "3opt" : 0,
    "2opt" : 0,
    "switch_two_deliveries_with_routes" : 0,
    "reverse_same_route" : 0,
    "relocate" : 0
}

def tabu_search(vrptw : VRPTW, size_tabu = SIZE_TABU) -> Tuple[VRPTW, int] :
    global selected_action
    global unselected_action

    x_min = vrptw
    f_min = fitness(vrptw)
    tabu = []
    print(f"initial : {f_min}")
    initial = f_min
    previous_x = None
    for i in range(1000) :
        print(i)
        current_x, f_current_x, action = get_neighborhood_without_tabu_list(vrptw, tabu)
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
                tabu.append(action)
                if(len(tabu) > size_tabu):
                    tabu.pop(0)
        if f_current_x < f_min :
            # print(f"old best : {f_min} ")
            x_min = current_x
            f_min = f_current_x
            print(f"new best : {f_min} ")

        previous_x = current_x

    print(f"selected_action {selected_action} unselected_action {unselected_action}")
    print(f"ecart : {initial - f_min}")
    print(f"meilleure fitness : {f_min}")
    print(method_used)
    return x_min, f_min

def get_neighborhood_without_tabu_list(vrptw : VRPTW, tabu):
    global method_used

    operators = [
        get_neighborhood_without_tabu_list_opt2, 
        get_neighborhood_without_tabu_list_opt3, 
        get_neighborhood_without_tabu_list_random_switch_two_deliveries_with_routes, 
        get_neighborhood_without_tabu_list_random_reverse_same_route,
     #   get_neighborhood_without_tabu_list_relocate # Commentée en attendant que Greg trouve ce qui se passe
    ]
    
    # operators = [get_neighborhood_without_tabu_list_random_reverse_same_route]
    best_neighbor = None
    best_f = 10000000
    best_action = None

    for operator in operators:
        neighbor, f, action = operator(copy.deepcopy(vrptw), tabu)
        print(action[0], f)
        if f != None and f < best_f :
            best_f = f
            best_action = action
            best_neighbor = neighbor
    method_used[best_action[0]] += 1

    return best_neighbor, best_f, best_action

def get_neighborhood_without_tabu_list_relocate(vrptw: VRPTW, tabu):
    best_f = None
    best_action = None
    best_neighbor = None
    vrptw = copy.deepcopy(vrptw)
    for route1 in vrptw.routes :
        j=0
        for delivery1 in route1.path :
            for route2 in vrptw.routes :
                i = 0
                for delivery2 in route2.path[:-1] :
                    i += 1
                    previous = delivery2
                    next = route2.path[i]
                    action = ("relocate", route1.route_id, route2.route_id, j, i-1)
                    if action in tabu: # TODO : aussi vérifier dans l'autre sens (inverser routes et clients)
                        # Le tirage est invalide, on continue
                        continue
                    relocate_delivery(vrptw.routes, delivery1, vrptw.warehouse, previous, next )
                    f_neigbhor = fitness(vrptw)
                    # print("relocate : ", j, i-1, route1.route_id, route2.route_id, f_neigbhor)
                    if best_f is None or f_neigbhor < best_f :
                        best_neighbor = vrptw
                        best_action = action
                        best_f = f_neigbhor
                    vrptw = copy.deepcopy(vrptw)
            j+=1
            
    # for _ in range(1000):
    #     vrptw = copy.deepcopy(vrptw)
    #     route1 = vrptw.get_random_route()
    #     route2 = vrptw.get_random_route()

    #     d1 = route.get_random_delivery_index()
    #     d2 = route2.get_random_delivery_index()
    #     action = ("relocate_extra", route.route_id, d1, d2)
    #     if action in tabu: # TODO : aussi vérifier dans l'autre sens (inverser routes et clients)
    #         # Le tirage est invalide, on continue
    #         continue
    #     relocate_delivery(vrptw.routes, d1, d2vrptw.warehouse, )
    #     f_neigbhor = fitness(vrptw)
    #     if best_f is None or f_neigbhor < best_f :
    #         best_neighbor = vrptw
    #         best_action = action
    #         best_f = f_neigbhor
    
    return best_neighbor, best_f, best_action

def get_neighborhood_without_tabu_list_random_reverse_same_route(vrptw: VRPTW, tabu):
    best_f = None
    best_action = None
    best_neighbor = None
    for _ in range(1000):
        vrptw = copy.deepcopy(vrptw)
        route = vrptw.get_random_route()
        d1 = route.get_random_delivery_index()
        d2 = route.get_random_delivery_index()
        action = ("reverse_same_route", route.route_id, d1, d2)
        if action in tabu: # TODO : aussi vérifier dans l'autre sens (inverser routes et clients)
            # Le tirage est invalide, on continue
            continue
        reverse_in_same_route(route, vrptw.warehouse, )
        f_neigbhor = fitness(vrptw)
        if best_f is None or f_neigbhor < best_f :
            best_neighbor = vrptw
            best_action = action
            best_f = f_neigbhor
    return best_neighbor, best_f, best_action

def get_neighborhood_without_tabu_list_random_switch_two_deliveries_with_routes(vrptw : VRPTW, tabu):
    # Faire une deep copy de routes avant de la modifier
    best_f = None
    best_action = None
    best_neighbor = None
    # for operator in allowed_operators:
    for _ in range(10):
        vrptw = copy.deepcopy(vrptw)
        # print(f"n : {i}")
            # Attention, pour le reverse il faut qu'ils soient dans la même route
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

selected_action = 0
unselected_action = 0

def get_neighborhood_without_tabu_list_opt2(vrptw : VRPTW, tabu):
    '''
    récupère le voisin avec la meilleur fitness
    '''
    global selected_action
    global unselected_action
    # Faire une deep copy de routes avant de la modifier
    best_f = None
    best_action = None
    best_neighbor = None
    vrptw_copy = vrptw # TODO : to remove # copy.deepcopy(vrptw)
    for couple in generate_2opt_couples(vrptw_copy.routes):
        route_index = couple[2]
        action = ("2opt", route_index, couple[0], couple[1])
        if action in tabu:
            unselected_action += 1
            # Le tirage est invalide, on saute cett itération
            continue
        selected_action += 1
        
        routes_copy = copy.deepcopy(vrptw_copy.routes)
        
        switch_two_deliveries_in_same_route(routes_copy[route_index], couple[0], couple[1], vrptw_copy.warehouse)  

        # vrptw_copy_copy = copy.deepcopy(vrptw_copy)
        # vrptw_copy_copy.routes = routes_copy

        f_neigbhor = fitness_vrptwless(routes_copy, vrptw_copy.warehouse)

        if best_f is None or f_neigbhor < best_f :
        
            best_neighbor = vrptw_copy
            best_action = action
            best_f = f_neigbhor
            
    return best_neighbor, best_f, best_action

def get_neighborhood_without_tabu_list_opt3(vrptw : VRPTW, tabu):
    '''
    récupère le voisin avec la meilleur fitness
    '''
    global selected_action
    global unselected_action
    # Faire une deep copy de routes avant de la modifier
    best_f = None
    best_action = None
    best_neighbor = None
    vrptw_copy = vrptw # TODO : to remove # copy.deepcopy(vrptw)
    for couple in generate_3opt_couples(vrptw_copy.routes):
        route_index = couple[2]
        action = ("3opt", route_index, couple[0], couple[1])
        if action in tabu:
            unselected_action += 1
            # Le tirage est invalide, on saute cette itération
            continue
        selected_action += 1
        
        routes_copy = copy.deepcopy(vrptw_copy.routes)
        
        switch_two_deliveries_in_same_route(routes_copy[route_index], couple[0], couple[1], vrptw_copy.warehouse)  

        # vrptw_copy_copy = copy.deepcopy(vrptw_copy)
        # vrptw_copy_copy.routes = routes_copy

        f_neigbhor = fitness_vrptwless(routes_copy, vrptw_copy.warehouse)

        if best_f is None or f_neigbhor < best_f :
        
            best_neighbor = vrptw_copy
            best_action = action
            best_f = f_neigbhor
            
    return best_neighbor, best_f, best_action

# function(routes, warehouse, delivery_1, **{random.choice["delivery_next","delivery_previous"]:delivery_2})
# *[]
