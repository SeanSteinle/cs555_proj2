from router import Router
from network_topology import read_nodes

#reading nodes
print(f"reading data...")
nodes = read_nodes('network.txt')
print(f"done!")

print(f"starting routers...")
Router.start_routers(nodes)
print(f"done!")