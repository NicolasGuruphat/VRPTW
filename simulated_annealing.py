from random_solution import random_solution
from config import SIMULATED_ANNEALING_DELTA_F_SAMPLE
from model.VRPTW import VRPTW
from utils import fitness_vrptwless, fitness, exchange_route_chunk, switch_two_deliveries, reverse, relocate_delivery
from math import log, exp, sqrt
from copy import deepcopy
import random
import csv
import sys
from printer.printer import display_vrp
import time

ALLOWED_OPERATORS = {
    # exchange_route_chunk: [2, 4],
    switch_two_deliveries: [2],
    # reverse: [1],
    relocate_delivery: [2],
}

OPT_MAP = {
    "R": {
        # exchange_route_chunk: [2, 4],
        # switch_two_deliveries: [2],
        # reverse: [1],
        relocate_delivery: [2],
    }, "RS": {
        # exchange_route_chunk: [2, 4],
        switch_two_deliveries: [2],
        # reverse: [1],
        relocate_delivery: [2],
    }, "RE": {
        exchange_route_chunk: [2, 4],
        # switch_two_deliveries: [2],
        # reverse: [1],
        relocate_delivery: [2],
    }, "RSE": {
        exchange_route_chunk: [2, 4],
        switch_two_deliveries: [2],
        # reverse: [1],
        relocate_delivery: [2],
    }, "RI": {
        # exchange_route_chunk: [2, 4],
        # switch_two_deliveries: [2],
        reverse: [1],
        relocate_delivery: [2],
    }, "RISE": {
        exchange_route_chunk: [2, 4],
        switch_two_deliveries: [2],
        reverse: [1],
        relocate_delivery: [2],
    }
}

fitnesses = []
BEST_AT = [0]

def get_random_neighbor(vrptw: VRPTW, opt = ALLOWED_OPERATORS) -> VRPTW:
    vrptw_copy = deepcopy(vrptw)

    error = True

    begin = time.time()

    while error:
        operator_to_use = random.choice(list(opt.keys()))

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

        if time.time() - begin >= 180:
            with open("./30_first_101/logs.csv", "a", newline="") as file:
                file.write(f"Timeout neighboor\n")
                break

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

def simulated_annealing(vrptw: VRPTW, t0_param: int = None, mu_param: float = None, n2_param: int = None, t_final: float = 0.001, **kwargs: dict) -> VRPTW:
    BEST_AT[0] = 0
    global fitnesses

    opt_to_use = {relocate_delivery:0,switch_two_deliveries:0,exchange_route_chunk:0} if kwargs.get("opt") == "RSE" else {relocate_delivery:0,switch_two_deliveries:0}

    initial_solution_routes = random_solution(vrptw)
    vrptw.routes = initial_solution_routes
    initial_solution_fitness = fitness(vrptw)
    # display_vrp(vrptw.warehouse, vrptw.customers, vrptw.routes)

    delta_fs = list()
    for _ in range(SIMULATED_ANNEALING_DELTA_F_SAMPLE):
        delta_fs.append(fitness_vrptwless(random_solution(vrptw), vrptw.warehouse))

    delta_f = sum([abs(delta_f_computed - initial_solution_fitness) for delta_f_computed in delta_fs]) / SIMULATED_ANNEALING_DELTA_F_SAMPLE

    t_0 = -(delta_f / log(0.8))
    if t_0 == 0:
        t_0 = 1
    
    # Should increase
    mu = 0.60
    if mu_param:
        mu = mu_param

    # n1 = log(log(0.8) / log(0.01)) / log(mu)
    way = kwargs.get("way")
    if way == "SQRT":
        n1 = sqrt(delta_f)
    elif way == "LN":
        n1 = log(delta_f)
    elif way == "2SQRT":
        n1 = 2 * sqrt(delta_f)
    elif way == "10SQRT":
        n1 = 10 * sqrt(delta_f)
    elif way == "2LN":
        n1 = 2 * log(delta_f)
    else:
        n1 = sqrt(delta_f)

    mu = exp((log(t_final) - log(t_0)) / n1)

    n2 = 10000
    if n2_param:
        n2 = n2_param
    n_no_upgrade_max = 10000

    x_min = deepcopy(vrptw)
    x_current = x_min
    f_min = initial_solution_fitness
    f_current = initial_solution_fitness
    i = 0
    ####################################
    # t_0 = 80
    # if t0_param:
    #     t_0 = t0_param
    ####################################
    t_k = t_0

    print(f"TI {t_0}")
    print(f"MU {mu}")
    print(f"DF {delta_f}")

    fitnesses = []

    fitnesses.append(f_current)

    for k in range(int(n1)):
        print(f"{k}/{int(n1)}")
        no_upgrade = 0
        begin = time.time()
        for l in range(1, int(n2)):
            # sys.stdout.write("\r{0}>".format(l))
            # sys.stdout.flush()

            y = get_random_neighbor(x_current, opt=opt_to_use)

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
                    BEST_AT[0] = k * n2 + l
            else:
                no_upgrade += 1
                p = random.random()
                if p <= exp(-delta_f_current/t_k):
                    x_current = deepcopy(y)
                    f_current = f_y
            i += 1
            if time.time() - begin >= 180:
                with open("./100_first_101_tw/logs.csv", "a", newline="") as file:
                    file.write(f"Timeout {k} / {n1}; {l} {mu} {t_k}\n")
                    fitnesses.append(f_current)
                    break

            fitnesses.append(f_current)
        t_k *= mu
        mu *= 0.95
        print(f"Meilleur {f_min}")
        if no_upgrade >= n_no_upgrade_max:
            continue

    return (x_min, mu, t_0, n1) if kwargs.get("return_mu") else x_min

# VRPTW_ = VRPTW('data101 short.vrp')

SIM = True

mus_full = [0.5,0.6,0.7,0.75,0.8,0.85,0.9,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99]
mus = [mus_full[5]]

files = [
    "101",
    # "101 short",
    # "102",
    # "102 short",
    # "111",
    # "111 short",
    # "112",
    # "112 short",
    # "201",
    # "201 short",
    # "202",
    # "202 short",
    # "1101",
    # "1101 short",
    # "1102",
    # "1102 short",
    # "1201",
    # "1201 short",
    # "1202",
    # "1202 short",
]

if SIM:
    for data_file in files:
        VRPTW_ = VRPTW(f'data{data_file}.vrp')
        last_line = None
        try:
            with open(f"./no_matter/sim_{data_file}.csv", "r", newline="") as file:
                lines = file.readlines()
                if len(lines) >= 2:
                    last_line = lines[-1]
        except Exception:
            pass
        if not last_line:
            with open(f"./no_matter/sim_{data_file}.csv", "w", newline="") as file:
                csv.writer(file).writerow(["AVG_MU", "MIN_MU", "MAX_MU", "OPT_USED", "N2", "AVG_T0", "MIN_T0", "MAX_T0", "F0", "F_AVG", "F_MIN", "F_MAX", "AVG_BEST_AT", "MIN_BEST_AT", "MAX_BEST_AT", "INIT_NB_TRUCKS", "AVG_NB_TRUCKS", "MIN_NB_TRUCKS", "MAX_NB_TRUCKS", "AVG_EXEC_T", "MIN_EXEC_T", "MAX_EXEC_T","AVG_N1", "MIN_N1", "MAX_N1", "WAY"])

        params = list()
        # opt_used = ["RSE"]
        opt_used = ["RS"]
        # opt_used = ["RS", "RSE"]
        # opt_used = ["R", "RS", "RE", "RSE", "RI", "RISE"]
        n2s = [10000]
        # n2s = [10000, 1000]
        way_to_get_n1 = ["SQRT"]
        # way_to_get_n1 = ["SQRT", "LN", "2SQRT", "2LN"]
        t_n1s = [0.86]
        # t_n1s = [0.86]
        # t0s = [3,4,5,6,7,8,9,10,15,20,25,30,40,50,60,70,80,90,100,150,200,300,400,500,1000]

        for opt in opt_used:
            for n2 in n2s:
                for t_n1 in t_n1s:
                    for way in way_to_get_n1:
                        params.append((opt, n2, t_n1, way))

        last_dones = (0,0,0,0)
        if last_line:
            split_line = last_line.split(",")
            last_way = str(split_line[-1])
            last_opt = str(split_line[3])
            last_n2 = int(split_line[4])
            # last_t0 = int(split_line[3])
            last_dones = (last_opt, last_n2, t_n1s[0], last_way.split("/")[0])
        
        try:
            params = params[params.index(last_dones) + 1:]
        except ValueError:
            pass

        for param in params:
            opt = param[0]
            n2 = param[1]
            t_n1 = param[2]
            way = param[3]

            print(f"Doing {opt} {n2} {t_n1} {way}")

            # ALLOWED_OPERATORS = OPT_MAP.get(opt, {relocate_delivery: [2]})

            fs = list()
            trucks = list()
            best_ats = list()
            exec_times = list()
            computed_mus = list()
            t_0s = list()
            n_1s = list()
            for i in range(3):
                try:
                    begin = time.time_ns()
                    vrptw, computed_mu, computed_t0, computed_n1 = simulated_annealing(VRPTW_, n2_param=n2, t_final=t_n1, **{"opt": opt, "way": way, "return_mu": True})
                    computed_mus.append(computed_mu)
                    n_1s.append(computed_n1)
                    t_0s.append(computed_t0)
                    end = time.time_ns()
                    fs.append(fitness(vrptw))
                    best_ats.append(BEST_AT[0])
                    trucks.append(len(vrptw.routes))
                    exec_times.append(ex := end - begin)

                    with open("./fitness_evolution/evolution.json", "a") as evo_file:
                        evo_file.write(f'"{"c" if way == "SQRT" else "g"}{i}": ' + "{" + f'"f" : {fitnesses}, "e": {ex}' + "},")
                except Exception as e:
                    print(e)
                    continue

            if not fs or not best_ats or not trucks:
                print("Params gave no results")
                continue

            f0 = fitness(VRPTW_)
            f_avg = sum(fs) / len(fs)
            f_min = min(fs)
            f_max = max(fs)
            n1_avg = sum(n_1s) / len(n_1s)
            n1_min = min(n_1s)
            n1_max = max(n_1s)
            t0_avg = sum(t_0s) / len(t_0s)
            t0_min = min(t_0s)
            t0_max = max(t_0s)
            mu_avg = sum(computed_mus) / len(computed_mus)
            mu_min = min(computed_mus)
            mu_max = max(computed_mus)
            avg_best_at = sum(best_ats) / len(best_ats)
            min_best_at = min(best_ats)
            max_best_at = max(best_ats)
            init_nb_trucks = len(VRPTW_.routes)
            avg_nb_trucks = sum(trucks) / len(trucks)
            min_nb_trucks = min(trucks)
            max_nb_trucks = max(trucks)
            avg_exec_t = sum(exec_times) / len(exec_times)
            min_exec_t = min(exec_times)
            max_exec_t = max(exec_times)

            with open(f"./no_matter/sim_{data_file}.csv", "a", newline="") as file:
                csv.writer(file).writerow([mu_avg, mu_min, mu_max, opt, n2, t0_avg, t0_min, t0_max, f0, f_avg, f_min, f_max, avg_best_at, min_best_at, max_best_at, init_nb_trucks, avg_nb_trucks, min_nb_trucks, max_nb_trucks, avg_exec_t, min_exec_t, max_exec_t, n1_avg, n1_min, n1_max, way])


else:
    VRPTW_ = VRPTW("data101.vrp")
    begin = time.time()
    vrptw = simulated_annealing(VRPTW_, t_final=0.86)
    print(f"Time took : {time.time() - begin}")
    print(f"Fitness init {fitness(VRPTW_)}")
    print(f"Fitness computed {fitness(vrptw)}")
    from printer.printer import display_vrp
    print(f"BAT {BEST_AT}")
    print(f"Trucks init {len(VRPTW_.routes)}")
    print(f"Trucks computed {len(vrptw.routes)}")
    display_vrp(VRPTW_.warehouse, VRPTW_.customers, VRPTW_.routes)
    display_vrp(vrptw.warehouse, vrptw.customers, vrptw.routes)