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

print(f"initializing network graph...")
threads = network_init("network.txt")
#now can use thread.start(), thread.join() to synchronize. thread control should occur here, in main(?)