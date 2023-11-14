import threading
from router import Router
from socket_utils import start_main_socket, signal_router
from network_topology import read_nodes 

neighbors_dict = read_nodes('network.txt')
# print(neighbors_dict)

thread = threading.Thread(target=Router, args=(len(neighbors_dict.keys()), 0, neighbors_dict[0]))

thread.start()

s = start_main_socket(0)
response = signal_router(s, "update_table: data")
print(response)
