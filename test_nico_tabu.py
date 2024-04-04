from model.VRPTW import VRPTW
from metaheuristique import tabu_search
from random_solution import random_solution
vrptw = VRPTW('data111.vrp')
vrptw.routes = random_solution(vrptw)
print(tabu_search(vrptw))