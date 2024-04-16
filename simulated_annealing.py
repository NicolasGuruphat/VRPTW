from random_solution import random_solution
from config import SIMULATED_ANNEALING_DELTA_F_SAMPLE
from model.VRPTW import VRPTW
from utils import fitness_vrptwless, fitness, exchange_route_chunk, switch_two_deliveries, reverse, relocate_delivery
from math import log, exp
from copy import deepcopy
import random
import sys
from printer.printer import display_vrp

ALLOWED_OPERATORS = {
    # exchange_route_chunk: [2, 4],
    switch_two_deliveries: [2],
    # reverse: [1],
    relocate_delivery: [2],
}

def get_random_neighbor(vrptw: VRPTW) -> VRPTW:
    vrptw_copy = deepcopy(vrptw)

    error = True

    while error:
        operator_to_use = random.choice(list(ALLOWED_OPERATORS.keys()))

        if operator_to_use == relocate_delivery:
            error = not relocate_delivery(vrptw_copy.routes, random.choice(random.choice(vrptw_copy.routes).path), vrptw_copy.warehouse, **{random.choice(["delivery_new_previous", "delivery_new_next"]): random.choice(random.choice(vrptw_copy.routes).path)})
            # print(error)
        elif operator_to_use == switch_two_deliveries:
            error = not switch_two_deliveries(vrptw_copy.routes, random.choice(random.choice(vrptw_copy.routes).path), random.choice(random.choice(vrptw_copy.routes).path), vrptw_copy.warehouse)
        #     print(error)
        # elif operator_to_use == reverse:
        #     r = random.choice(vrptw_copy.routes)
        #     l = len(r.path)
        #     from_index = random.randint(0, l - 1)
        #     if from_index == l - 1:
        #         to_index = None
        #     else:
        #         to_index = random.randint(from_index + 1, l - 1) if from_index else random.randint(0, l - 1)
        #     error = not reverse(
        #         vrptw_copy.routes,
        #         vrptw_copy.warehouse,
        #         None if random.random() < 0.2 else r.path[from_index],
        #         None if from_index == l - 1 or from_index is None or random.random() < 0.2 else r.path[to_index]
        #     )
        elif exchange_route_chunk:
            r1 = random.choice(vrptw_copy.routes)
            l1 = len(r1.path)
            from_index1 = random.randint(0, l1 - 1)
            if from_index1 == l1 - 1:
                to_index1 = None
            else:
                to_index1 = random.randint(from_index1 + 1, l1 - 1) if from_index1 else random.randint(0, l1 - 1)

            routes_copy = vrptw_copy.routes.copy()
            routes_copy.remove(r1)
            r2 = random.choice(routes_copy)
            l2 = len(r2.path)
            from_index2 = random.randint(0, l2 - 1)
            if from_index2 == l2 - 1:
                to_index2 = None
            else:
                to_index2 = random.randint(from_index2 + 1, l2 - 1) if from_index2 else random.randint(0, l2 - 1)
            error = not exchange_route_chunk(
                vrptw_copy.routes,
                vrptw_copy.warehouse,
                None if random.random() < 0.2 else r1.path[from_index1],
                None if from_index1 == l1 - 1 or from_index1 is None or random.random() < 0.2 else r1.path[to_index1],
                None if random.random() < 0.2 else r2.path[from_index2],
                None if from_index2 == l2 - 1 or from_index2 is None or random.random() < 0.2 else r2.path[to_index2]
            )
        else:
            continue

    pl = 0
    for route in vrptw_copy.routes:
        pl += route.delivery_truck.package_left
    # print(f"PL {pl}")
    
    routes_copy = vrptw_copy.routes.copy()
    for route in vrptw_copy.routes:
        if len(route.path) == 0:
            print("EMPTY")
            routes_copy.remove(route)
    vrptw_copy.routes = routes_copy
    # print(f"NT {len(routes_copy)}")
    # print(vrptw.routes == vrptw_copy.routes)
    return vrptw_copy

def simulated_annealing(vrptw: VRPTW) -> VRPTW:
    initial_solution_routes = random_solution(vrptw)
    vrptw.routes = initial_solution_routes
    initial_solution_fitness = fitness(vrptw)
    display_vrp(vrptw.warehouse, vrptw.customers, vrptw.routes)

    delta_fs = list()
    for _ in range(SIMULATED_ANNEALING_DELTA_F_SAMPLE):
        delta_fs.append(fitness_vrptwless(random_solution(vrptw), vrptw.warehouse))

    delta_f = sum([abs(delta_f_computed - initial_solution_fitness) for delta_f_computed in delta_fs]) / SIMULATED_ANNEALING_DELTA_F_SAMPLE

    t_0 = -(delta_f / log(0.8))
    if t_0 == 0:
        t_0 = 1
    
    # Should increase
    mu = 0.90

    n1 = log(log(0.8) / log(0.01)) / log(mu)
    n2 = 10000
    n_no_upgrade_max = 10000

    x_min = deepcopy(vrptw)
    x_current = x_min
    f_min = initial_solution_fitness
    f_current = initial_solution_fitness
    i = 0
    ####################################
    t_0 = 80
    ####################################
    t_k = t_0

    print(f"TI {t_0}")

    for k in range(int(n1)):
        print(f"{k}/{int(n1)}")
        no_upgrade = 0
        for l in range(1, int(n2)):
            # sys.stdout.write("\r{0}>".format(l))
            # sys.stdout.flush()

            y = get_random_neighbor(x_current)

            f_y = fitness(y)
            delta_f_current = f_y - f_current
            # print(f"{k} {l} : {f_current} {f_y} {delta_f_current}")
            # if delta_f_current == 0:
            #     display_vrp(x_current.warehouse, x_current.customers, x_current.routes)
            #     display_vrp(y.warehouse, y.customers, y.routes)

            if delta_f_current <= 0:
                f_current = f_y
                x_current = deepcopy(y)
                if f_y < f_min:
                    x_min = deepcopy(y)
                    f_min = f_y
            else:
                no_upgrade += 1
                p = random.random()
                if p <= exp(-delta_f_current/t_k):
                    x_current = deepcopy(y)
                    f_current = f_y
            i += 1
        t_k *= mu
        mu *= 0.95
        print(f"Meilleur {f_min}")
        if no_upgrade >= n_no_upgrade_max:
            continue
    return x_min

VRPTW_ = VRPTW('data101 short.vrp')
vrptw = simulated_annealing(VRPTW_)
print(fitness(VRPTW_))
print(fitness(vrptw))
from printer.printer import display_vrp
print(len(VRPTW_.routes))
print(len(vrptw.routes))
display_vrp(VRPTW_.warehouse, VRPTW_.customers, VRPTW_.routes)
display_vrp(vrptw.warehouse, vrptw.customers, vrptw.routes)