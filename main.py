from Parser import parse_vrptw_file
from printer.printer import display_vrp
from model.DeliveryTruck import DeliveryTruck
from model.Route import Route
from random import randint

path = 'data/data101.vrp'

# print(parse_vrptw_file(path))
(   
    _,
    warehouse_number,
    customer_number,
    truck_package_limit, 
    warehouses,
    customers
)= parse_vrptw_file(path)

dt1 = DeliveryTruck(truck_package_limit)
dt2 = DeliveryTruck(truck_package_limit)
dt3 = DeliveryTruck(truck_package_limit)

r1 = Route(dt1)
r2 = Route(dt2)
r3 = Route(dt3)
lr = [r1, r2, r3]

tmp_customer_list = customers.copy()
for r in lr:
    for i in range(25):
        rand = randint(0, len(tmp_customer_list) - 1)
        r.add(tmp_customer_list[rand])
        del tmp_customer_list[rand]

display_vrp(warehouses[0], customers, lr)