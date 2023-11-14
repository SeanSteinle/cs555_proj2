from router import Router
from network_topology import network_init
import socket, time

timeout = 1

#reading nodes
print(f"loading data...")
threads = network_init('network.txt')
print(f"data loaded!")

#starting threads
for thread in threads:
    thread.start()

#let threads execute until TIMEOUT
time.sleep(timeout)

#can now end server sockets by issuing "end" commands!
print("Final output: ")
for router_n in range(len(threads)):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((socket.gethostname(), 50000+router_n))
    client.sendall(b'end,0,0')
    client.close()

time.sleep(0.1) #let threads close peacefully
print(f"Number of rounds till convergence {Router.round_n}")

#end threads -- will likely need to issue close condition
for thread in threads:
    thread.join()