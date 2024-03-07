from model.VRPTW import VRPTW
from model.DeliveryTruck import DeliveryTruck
from model.Route import Route
import random as r
import math

VRPTW = VRPTW('data111.vrp')

totalServiceTime = 0

for customers in VRPTW.customers:
    totalServiceTime += customers.service

minTruckNumber = math.ceil((totalServiceTime) / (VRPTW.warehouse.due_time - VRPTW.warehouse.ready_time))

trucks = []
routes = []
for _ in range(minTruckNumber):
    delivery_truck = DeliveryTruck(VRPTW.truck_package_limit)
    trucks.append(delivery_truck)
    routes.append(Route(delivery_truck))

customers_left = VRPTW.customers.copy()
for route in routes:
    # assignation des 
    picked_truck = r.randint(0,len(trucks)-1)
    route.truck = trucks[picked_truck] 
    current_truck = route.truck
    trucks.pop(picked_truck)
    current_time = 0
    while(
        current_truck.package_left > current_truck.package_limit * 0.8 # on ne remplit les camions qu'à 80%
        and len(customers_left) > 0 
        and current_time < VRPTW.warehouse.due_time
        ): 
        for customer in customers_left:
            if (
                customer.ready_time >= current_time 
                and current_time + customer.service <=  VRPTW.warehouse.due_time
                and  customer.demand <= current_truck.package_left
                ):
                print("here")
                route.add(customer)
                current_time += customer.service
                customers_left.pop(customers_left.index(customer))
            elif(customer.ready_time >= current_time ):
                # on ajoute pour éviter que le camion attende indéfiniment
                current_time += 10
            # else:
            #     print(customer.ready_time, current_time, customer.ready_time >= current_time)
        print(len(customers_left))
    if(len(customers_left) == 0):
        break
