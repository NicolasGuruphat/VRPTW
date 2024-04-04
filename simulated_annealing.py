from random_solution import random_solution
from config import SIMULATED_ANNEALING_DELTA_F_SAMPLE
from model.VRPTW import VRPTW
from utils import fitness_vrptwless, fitness
from math import ln

def simulated_annealing(vrptw: VRPTW) -> VRPTW:
    initial_solution_routes = random_solution(vrptw)
    vrptw.routes = initial_solution_routes
    initial_solution_fitness = fitness(vrptw)

    delta_fs = list()
    for _ in range(SIMULATED_ANNEALING_DELTA_F_SAMPLE):
        delta_fs.append(fitness_vrptwless(random_solution(vrptw)))

    delta_f = sum([abs(delta_f_computed - initial_solution_fitness) for delta_f_computed in delta_fs]) / SIMULATED_ANNEALING_DELTA_F_SAMPLE

    t_0 = -(delta_f / ln(0.8))
    
    # Should increase
    mu = 0.1

    n1 = ln(ln(0.8) / ln(0.01)) / ln(mu)