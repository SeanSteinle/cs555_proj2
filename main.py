from router import Router
from network_topology import network_init
import socket

#reading nodes
print(f"reading data...")
threads = network_init('network.txt')
print(f"done!")

#starting threads
for thread in threads:
    thread.start()

import time
time.sleep(5)

#can now end server sockets by issuing "end" commands!
for router_n in range(len(threads)):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((socket.gethostname(), 50000+router_n))
    client.sendall(b'end,0,0')
    client.close()

#end threads -- will likely need to issue close condition
for thread in threads:
    thread.join()