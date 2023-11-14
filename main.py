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
time.sleep(3)

#can now check for end of propogation via "has_updates?" command!
for router_n in range(len(threads)):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((socket.gethostname(), 50000+router_n))
    client.sendall(b'has_updates?,0,0')
    response = client.recvfrom(1024)
    print(f"router #{router_n} has more updates? {response}")
    client.close()

time.sleep(3)

#can now end server sockets by issuing "end" commands!
for router_n in range(len(threads)):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((socket.gethostname(), 50000+router_n))
    client.sendall(b'end,0,0')
    client.close()

#end threads -- will likely need to issue close condition
for thread in threads:
    thread.join()