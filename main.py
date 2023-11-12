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
from socket_utils import signal_router

#parse network map, create thread objects of Routers
print(f"initializing network graph...")
threads = network_init("network.txt")

#start Router threads
for thread in threads:
    thread.start()

#main iteration loop
n_iterations = 5
for iter_n in range(n_iterations):
    curr_router_id = iter_n % len(threads) #TD: actually, this should be a lookup!
    print(f"iteration #{iter_n}. signaling router #{curr_router_id}")
    response = signal_router(curr_router_id)
    print(f"got response {response}")
    #assert response == "success"