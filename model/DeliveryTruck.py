from typing import List


class DeliveryTruck:
    package_limit: int
    package_left: int

    def __init__(self, package_limit: int):
        self.package_limit = package_limit
        self.package_left = self.package_limit
    
    def __repr__(self) -> str:
        return '{"__type": DeliveryTruck", "package_limit": ' + str(self.package_limit) + '", "package_left": "' + str(self.package_left) + '"}'

    def load(self, packages):
        self.package_left -= packages