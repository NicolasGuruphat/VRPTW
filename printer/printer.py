from typing import List
import matplotlib.pyplot as plt
import networkx as nx
from networkx import Graph, DiGraph
from model.Warehouse import Warehouse
from model.Customer import Customer
from model.Route import Route


class PrintGraph(DiGraph):
    """
    Example subclass of the Graph class.

    Prints activity log to file or standard output.
    """

    def __init__(self, data=None, name="", file=None, **attr):
        super().__init__(data=data, name=name, **attr)
        if file is None:
            import sys

            self.fh = sys.stdout
        else:
            self.fh = open(file, "w")

    def add_node(self, n, attr_dict=None, **attr):
        super().add_node(n, attr_dict=attr_dict, **attr)
        # self.fh.write(f"Add node: {n}\n")

    def add_nodes_from(self, nodes, **attr):
        for n in nodes:
            self.add_node(n, **attr)

    def remove_node(self, n):
        super().remove_node(n)
        # self.fh.write(f"Remove node: {n}\n")

    def remove_nodes_from(self, nodes):
        for n in nodes:
            self.remove_node(n)

    def add_edge(self, u, v, attr_dict=None, **attr):
        super().add_edge(u, v, attr_dict=attr_dict, **attr)
        # self.fh.write(f"Add edge: {u}-{v}\n")

    def add_edges_from(self, ebunch, attr_dict=None, **attr):
        for e in ebunch:
            u, v = e[0:2]
            self.add_edge(u, v, attr_dict=attr_dict, **attr)

    def remove_edge(self, u, v):
        super().remove_edge(u, v)
        # self.fh.write(f"Remove edge: {u}-{v}\n")

    def remove_edges_from(self, ebunch):
        for e in ebunch:
            u, v = e[0:2]
            self.remove_edge(u, v)

    def clear(self):
        super().clear()
        # self.fh.write("Clear graph\n")


def display_vrp(warehouse: Warehouse, customers: List[Customer], routes: List[Route]) -> None:
    G = PrintGraph()
    positions = dict()
    colors = list()
    current_color = 125
    color_offset = int(8192875 / len(routes))

    G.add_node(warehouse.id_name, label = "WH")
    positions[warehouse.id_name] = [warehouse.x, warehouse.y]

    for customer in customers:
        G.add_node(customer.id_name, label = customer.id_name)
        positions[customer.id_name] = [customer.x, customer.y]

    for route in routes:
        hex_color = "#" + hex(current_color).replace("0x", "").capitalize().ljust(6, "0")
        # print(f"Color: {hex_color}")

        for delivery_index in range(len(route.path) - 1):
            G.add_edge(route.path[delivery_index].customer.id_name, route.path[delivery_index + 1].customer.id_name)
            colors.append(hex_color)
        
        current_color += color_offset

    nx.draw(G, positions, with_labels=True, arrows=True, edge_color = colors, connectionstyle="arc3,rad=0.5", font_size=9)
    # nx.draw_networkx()
    plt.show()