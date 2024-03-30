from model.Customer import Customer

class Delivery:
    def __init__(self, customer: Customer, delivery_time: int) -> None:
        self.customer = customer
        self.delivery_time = delivery_time

    @property
    def departure(self):
        return self.delivery_time + self.customer.service
    
    @property
    def is_on_time(self):
        return self.delivery_time >= self.customer.ready_time and self.delivery_time <= self.customer.due_time
    
    def __repr__(self) -> str:
        return '{"__type": "Delivery", "delivery_time":"' + str(self.delivery_time) + '", "departure": "' + str(self.departure) + '", "customer": ' + str(self.customer) + '}'