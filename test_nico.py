from model.Route import Route
from model.DeliveryTruck import DeliveryTruck
from model.Delivery import Delivery
from model.Customer import Customer
from model.Warehouse import Warehouse
from printer.printer import display_vrp
from utils import switch_two_deliveries_in_same_route, total_distance

def generate_route(deliveries):
    t = DeliveryTruck(0)
    r = Route(t)
    for delivery in deliveries:
        r.add(delivery)
    return r

w = Warehouse(1,3,3,0,0)

c1 = Customer("1",0,0,0,0,0,0)
c2 = Customer("2",1,0,0,0,0,0)
c3 = Customer("3",0,1,0,0,0,0)

customers = [c1, c2, c3]

d1 = Delivery(c1,0)
d2 = Delivery(c2,0)
d3 = Delivery(c3,0)

deliveries = [d1, d2, d3]

route = generate_route(deliveries)

couples = []

# create every couple of two deliveries
for delivery_one in deliveries:
    for delivery_two in deliveries:
        if delivery_one != delivery_two and (delivery_one, delivery_two) not in couples and (delivery_two, delivery_one) not in couples:
            couples.append((delivery_one, delivery_two))

# for couple in couples:
#     print(couple[0].customer.id_name, couple[1].customer.id_name)

neighbors = []

# call switch_two_deliveries_in_same_route for every couple
for couple in couples:
    r = generate_route(deliveries) 
    neighbors.append([switch_two_deliveries_in_same_route(r, couple[0], couple[1])])

for neighbor in neighbors:
    display_vrp(w, customers, neighbor)
    print(total_distance(neighbor[0]))
