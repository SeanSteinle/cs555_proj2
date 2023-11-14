from routerTyler import Router
from network_topology import read_nodes

nodes = read_nodes('network.txt')

# print(nodes)

#start 3 routers with different parameters then let them go
Router.start_n_routers(nodes)