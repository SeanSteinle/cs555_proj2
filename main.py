#step 1: read network topology. should be implemented as network_init():
# read in network
    # can read from "network.txt".
    # should read into NxN array (N will always be 5, but the topology may be different)
# now spin up a thread for each node (N nodes, again N = 5)
    # when creating each node, pass a list of tuples containing each neighbor and its weight
# done! now let the individual threads run.

#step 2: nodal operations
# the DV matrix
    # each node has a NxN matrix where 

from network_topology import network_init
from socket_utils import start_main_socket, signal_router

#parse network map, create thread objects of Routers
print(f"initializing network graph...")
threads = network_init("network.txt")

#start Router threads
for thread in threads:
    thread.start()

#start main client sockets -- note that we keep sockets in a list instead of a dict. this is because our ids are just indices in this list.
main_clients = [start_main_socket(router_id) for router_id in range(len(threads))]

#main iteration loop
n_iterations = 5
for iter_n in range(n_iterations):
    curr_router_id = iter_n % len(threads)
    print(f"iteration #{iter_n}. signaling router #{curr_router_id}")
    response = signal_router(main_clients[curr_router_id], "share_table")
    print(f"(main) got response {response}")

print(f"closing main clients...")
for main_client in main_clients:
    main_client.close()

#main iteration loop
print("reconnecting to thread servers...")
main_clients = [start_main_socket(router_id) for router_id in range(len(threads))]

n_iterations = 5
for iter_n in range(n_iterations):
    curr_router_id = iter_n % len(threads)
    print(f"iteration #{iter_n}. signaling router #{curr_router_id}")
    response = signal_router(main_clients[curr_router_id], "share_table")
    print(f"(main) got response {response}")

print(f"closing main clients...")
for main_client in main_clients:
    main_client.close()

#TESTING UPDATE TABLE -- NOT FINISHED!:
#print(f"testing update...")
#response = signal_router(main_clients[0], "update_table: DATA HERE")
#print(f"(main) got response {response}")

print(f"closing threads...")
for thread in threads:
    thread.join()