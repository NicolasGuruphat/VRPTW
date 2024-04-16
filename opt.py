def generate_2opt_couples(routes):
    # TODO : check couples 
    couples = []
    for j, route in enumerate(routes):
        deliveries = route.path
        deliveries_size = len(deliveries) 
        for i in range( deliveries_size - 1 ):
            there_is_a_before = i > 0
            there_is_an_after = i+2 < deliveries_size
            if there_is_a_before and there_is_an_after:
                delivery_one = i
                delivery_two = i+1
                couples.append((delivery_one, delivery_two, j))
    # print(len(couples))
    return couples


def generate_3opt_couples(routes):
    couples = []
    for j, route in enumerate(routes):
        deliveries = route.path
        deliveries_size = len(deliveries) 
        for i in range( deliveries_size - 1 ):
            there_is_a_before = i > 0
            there_is_an_after = i+3 < deliveries_size
            if there_is_a_before and there_is_an_after:
                delivery_one = i
                delivery_two = i+2
                couples.append((delivery_one, delivery_two, j))
                
    return couples
def print_couples(couples):
    print("couples")
    for couple in couples:
        print(couple[0].customer.id_name, couple[1].customer.id_name)

