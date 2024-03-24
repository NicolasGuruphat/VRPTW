'''
ordre de récupération des données : 
NB_CLIENTS
'''
from typing import List, Dict, Tuple

from model.Warehouse import Warehouse
from model.Customer import Customer

def parse_vrptw_file(path: str) -> Tuple[Dict[str, str], int, int, int, List[Warehouse], List[Customer]]:


    file_metadata: Dict[str, str]

    warehouse_number: int
    customer_number: int
    truck_package_limit: int

    warehouses: List[Warehouse] = list()
    customers: List[Customer] = list()

    with open(path, 'r') as f:
        # File metadata
        file_metadata = {
            "name": f.readline().split(":")[-1].strip(),
            "comment": f.readline().split(":")[-1].strip(),
            "type": f.readline().split(":")[-1].strip(),
            "coordinate_type": f.readline().split(":")[-1].strip(),
        }

        # Global constants
        warehouse_number = int(f.readline().split(":")[-1].strip())
        customer_number = int(f.readline().split(":")[-1].strip())
        truck_package_limit = int(f.readline().split(":")[-1].strip())

        # Skipping black line
        f.readline()

        # Warehouse data
        f.readline()
        warehouses.append(Warehouse(*f.readline().strip().split(" ")))

        # Skipping black line
        f.readline()
        
        # Customer data
        f.readline()

        while line := f.readline() :
            customers.append(Customer(*line.split(" ")))

    return file_metadata, warehouse_number, customer_number, truck_package_limit, warehouses, customers