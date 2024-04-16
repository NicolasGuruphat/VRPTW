from model.VRPTW import VRPTW
from tabu import tabu_search
from random_solution import random_solution
from printer.printer import display_vrp

vrptw = VRPTW('data101_short.vrp')

vrptw.routes = random_solution(vrptw)
# display_vrp(vrptw.warehouse, vrptw.customers, vrptw.routes, False, False)
print(tabu_search(vrptw))
display_vrp(vrptw.warehouse, vrptw.customers, vrptw.routes, False, False)

'''
# Vérification du 2 opt

couples = generate_2opt_couples(vrptw.routes)
print_couples(couples)
print(len(couples))
print(sum([len(route.path) for route in vrptw.routes])-len(vrptw.routes))
'''