from model.VRPTW import VRPTW
from model.DeliveryTruck import DeliveryTruck
from model.Route import Route
from model.Delivery import Delivery
from model.Customer import Customer
import random as rand
import math
from printer.printer import display_vrp
from utils import get_time_between, switch_two_deliveries, relocate_delivery, reverse, exchange_route_chunk
from typing import List
# VRPTW_ = VRPTW('data111.vrp')
VRPTW_ = VRPTW('data_test.vrp')

w = VRPTW_.warehouse
t1 = DeliveryTruck(VRPTW_.truck_package_limit)
t2 = DeliveryTruck(VRPTW_.truck_package_limit)
t3 = DeliveryTruck(VRPTW_.truck_package_limit)
r1 = Route(t1)
r2 = Route(t2)
r3 = Route(t3)
c1 = VRPTW_.customers[0]
c2 = VRPTW_.customers[1]
c3 = VRPTW_.customers[2]
c4 = VRPTW_.customers[3]
c5 = VRPTW_.customers[4]
c6 = VRPTW_.customers[5]
c7 = VRPTW_.customers[6]
c8 = VRPTW_.customers[7]
c9 = VRPTW_.customers[8]
c10 = VRPTW_.customers[9]
d1 = Delivery(c1, get_time_between(w.x, w.y, c1.x, c1.y))
d2 = Delivery(c2, d1.departure + get_time_between(c1.x, c1.y, c2.x, c2.y))
d3 = Delivery(c3,  d2.departure + get_time_between(c2.x, c2.y, c3.x, c3.y))
d4 = Delivery(c4, get_time_between(w.x, w.y, c4.x, c4.y))
d5 = Delivery(c5,  d4.departure + get_time_between(c4.x, c4.y, c5.x, c5.y))
d6 = Delivery(c6,  d5.departure + get_time_between(c5.x, c5.y, c6.x, c6.y))
d7 = Delivery(c7,  d6.departure + get_time_between(c6.x, c6.y, c7.x, c7.y))
d8 = Delivery(c8, get_time_between(w.x, w.y, c8.x, c8.y))
d9 = Delivery(c9,  d8.departure + get_time_between(c8.x, c8.y, c9.x, c9.y))
d10 = Delivery(c10,  d9.departure + get_time_between(c9.x, c9.y, c10.x, c10.y))
t1.load(c1.demand)
t1.load(c2.demand)
t1.load(c3.demand)
t2.load(c4.demand)
t2.load(c5.demand)
t2.load(c6.demand)
t2.load(c7.demand)
t3.load(c8.demand)
t3.load(c9.demand)
t3.load(c10.demand)
r1.add(d1)
r1.add(d2)
r1.add(d3)
r2.add(d4)
r2.add(d5)
r2.add(d6)
r2.add(d7)
r3.add(d8)
r3.add(d9)
r3.add(d10)
display_vrp(w, VRPTW_.customers, [r1, r2, r3], edge_label = True)
# switch_two_deliveries([r1, r2, r3], d1, d10, w)
# relocate_delivery([r1, r2, r3], d1, w,delivery_new_previous=d4)#, delivery_new_next=d6)#, d3)
# reverse([r1, r2, r3], w, d5, d5)
# exchange_route_chunk([r1, r2, r3], w, 
#                     delivery_from_one=d1,
#                     delivery_to_one=d2,
#                     delivery_from_two=d5,
#                     delivery_to_two=d6
#                     )
print(relocate_delivery([r1, r2, r3], d1, w,delivery_new_next=d1))
display_vrp(w, VRPTW_.customers, [r1, r2, r3], edge_label = True)