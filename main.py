from router import Router
from network_topology import network_init
import socket

wait_time = 2 #the amount of time we wait between checks to see if the game is over

#reading nodes
print(f"reading data...")
threads = network_init('network.txt')
print(f"done!")

#starting threads
for thread in threads:
    thread.start()

import time
time.sleep(2)

#can now check for end of propogation via "has_updates?" command!
converged = False
while not converged:
    print("checking for updates...")
    time.sleep(wait_time)
    responses = []
    for router_n in range(len(threads)):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((socket.gethostname(), 50000+router_n))
        client.sendall(b'has_updates?,0,0')
        response = client.recvfrom(1024)
        responses.append(str(response))
        print(f"router #{router_n} has more updates? {response}")
        client.close()

    #if any of the threads have not converged, we must continue!
    anyTrue = False
    for response in responses:
        if 'True' in response:
            anyTrue = True
    if anyTrue: 
        converged = False
        time.sleep(2)
    else: 
        converged = True

#can now end server sockets by issuing "end" commands!
print(f"closing server sockets...")
for router_n in range(len(threads)):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((socket.gethostname(), 50000+router_n))
    client.sendall(b'end,0,0')
    client.close()

#end threads -- will likely need to issue close condition
print(f"ending threads...")
for thread in threads:
    thread.join()