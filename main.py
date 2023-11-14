from router import Router
from network_topology import network_init

#reading nodes
print(f"reading data...")
threads = network_init('network.txt')
print(f"done!")

#starting threads
for thread in threads:
    thread.start()

#end threads -- will likely need to issue close condition
for thread in threads:
    thread.join()