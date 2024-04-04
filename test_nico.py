from model.Route import Route
from model.DeliveryTruck import DeliveryTruck
from model.Delivery import Delivery
from model.Customer import Customer
from model.Warehouse import Warehouse
from printer.printer import display_vrp
from utils import switch_two_deliveries_in_same_route, total_distance

def generate_route(deliveries):
    t = DeliveryTruck(100)
    r = Route(t)
    for delivery in deliveries:
        r.add(delivery)
        t.load(delivery.customer.demand)
    return r

def print_couples(couples):
    print("couples")
    for couple in couples:
        print(couple[0].customer.id_name, couple[1].customer.id_name)

w = Warehouse("W1",1,1,0,230)

c1 = Customer("1",0,0,0,230,1,1)
c2 = Customer("2",0,2,0,230,1,1)
c3 = Customer("3",1,2,0,230,1,1)
c4 = Customer("4",2,1,0,230,1,1)
c5 = Customer("5",1,0,0,230,1,1)

customers = [c1, c2, c3, c4, c5]

d1 = Delivery(c1,0)
d2 = Delivery(c2,0)
d3 = Delivery(c3,0)
d4 = Delivery(c4,0)
d5 = Delivery(c5,0)

deliveries = [d1, d2, d3, d4, d5]

route = generate_route(deliveries)

################ EVERY COMBINAISON ######################
'''

couples = []

# create every couple of two deliveries
for delivery_one in deliveries:
    for delivery_two in deliveries:
        if delivery_one != delivery_two and (delivery_one, delivery_two) not in couples and (delivery_two, delivery_one) not in couples:
            couples.append((delivery_one, delivery_two))
    
neighbors = []

# call switch_two_deliveries_in_same_route for every couple
for couple in couples:
    r = generate_route(deliveries) 
    neighbors.append([switch_two_deliveries_in_same_route(r, couple[0], couple[1])])

for neighbor in neighbors:
    display_vrp(w, customers, neighbor)
    print(total_distance(neighbor[0]))

'''
###################### 2-OPT ############################
    
couples = []

# generate 2-opt couples
for i in range( len(deliveries) - 1 ):
    there_is_a_before = i > 0
    there_is_an_after = i+2 < len(deliveries)
    if there_is_a_before and there_is_an_after:
        delivery_one = deliveries[i]
        delivery_two = deliveries[i+1]
        couples.append((delivery_one, delivery_two))

# start the neighbors list with current config to display_it at first
neighbors = [[generate_route(deliveries)]]

print(couples)
# call switch_two_deliveries_in_same_route for every couple
for couple in couples:
    r = generate_route(deliveries) 
    neighbors.append([switch_two_deliveries_in_same_route(r, route.path.index(couple[0]), route.path.index(couple[1]), w)])

print_couples(couples)

for neighbor in neighbors:
    display_vrp(w, customers, neighbor, edge_label=True)
    print(total_distance(neighbor[0]))