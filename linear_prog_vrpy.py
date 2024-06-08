from random_solution import random_solution
from config import SIMULATED_ANNEALING_DELTA_F_SAMPLE, TIME_BY_DISTANCE_UNIT
from model.VRPTW import VRPTW
from model.Customer import Customer
from utils import fitness_vrptwless, fitness, exchange_route_chunk, switch_two_deliveries, reverse, relocate_delivery, distance
from math import log, exp, sqrt
from copy import deepcopy
import random
import csv
import sys
from printer.printer import display_vrp
import time
from networkx import DiGraph
from vrpy import VehicleRoutingProblem
from typing import Tuple, Dict

def vrptw_to_vrpy(vrptw: VRPTW) -> Tuple[VehicleRoutingProblem, Dict[int, Customer]]:
    g = DiGraph()

    mapping_cust_id = {cust.id_name:id for id,cust in enumerate(vrptw.customers)}
    mapping_id_cust = {id:cust for id,cust in enumerate(vrptw.customers)}
    
    for customer in vrptw.customers:
        mapped_id = mapping_cust_id.get(customer.id_name)
        
        distance_warehouse = distance(vrptw.warehouse.x, vrptw.warehouse.y, customer.x, customer.y)

        g.add_edge("Source", mapped_id, cost=distance_warehouse)
        g.add_edge(mapped_id, "Sink", cost=distance_warehouse)

        g.edges["Source", mapped_id]["time"] = distance_warehouse * TIME_BY_DISTANCE_UNIT + customer.service
        g.edges["Source", mapped_id]["time"] = distance_warehouse * TIME_BY_DISTANCE_UNIT

        g.nodes[mapped_id]["demand"] = customer.demand

        for other_customer in vrptw.customers:
            if other_customer != customer:
                mapped_other_id = mapping_cust_id.get(other_customer.id_name)
        
                dist = distance(customer.x, customer.y, other_customer.x, other_customer.y)
        
                g.add_edge(mapped_id, mapped_other_id, cost=dist)
                g.edges[mapped_id, mapped_other_id]["time"] = dist * TIME_BY_DISTANCE_UNIT + other_customer.service

    prob = VehicleRoutingProblem(g, load_capacity=vrptw.truck_package_limit)
    prob.duration = vrptw.warehouse.due_time - vrptw.warehouse.ready_time
    return prob, mapping_id_cust


# VRPTW_ = VRPTW('data101.vrp')
VRPTW_ = VRPTW('data101 short.vrp')

prob, mapping = vrptw_to_vrpy(VRPTW_)
prob.solve(cspy=False)
print(prob.best_value)