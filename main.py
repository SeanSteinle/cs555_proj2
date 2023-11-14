from router import Router
from network_topology import read_nodes

nodes = read_nodes('network.txt')

Router.start_routers(nodes)