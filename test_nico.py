from model.Route import Route
from model.DeliveryTruck import DeliveryTruck
from model.Delivery import Delivery
from model.Customer import Customer
from model.Warehouse import Warehouse
from printer.printer import display_vrp
from utils import switch_two_deliveries_in_same_route

w = Warehouse(1,3,3,0,0)

t1 = DeliveryTruck(0)

route = Route(t1)

c1 = Customer(1,0,0,0,0,0,0)
c2 = Customer(1,1,0,0,0,0,0)
c3 = Customer(1,0,1,0,0,0,0)

customers = [c1,c2,c3]

d1 = Delivery(c1,0)
d2 = Delivery(c2,0)
d3 = Delivery(c3,0)

route.add(d1)
route.add(d2)
route.add(d3)

routes = [route]
display_vrp(w, customers, routes)
# switch_two_deliveries_in_same_route(route, d1, d2)


