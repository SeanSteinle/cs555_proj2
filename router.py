import threading
import select
import socket
import pickle

class Router:

    num_routers = 0                     #keeps track of the number of routers there should be
    all_listening = threading.Event()   #will wake up all threads when all listening sockets are up
    routers_listening = set()           #keeps track of the number of listening sockets are up
    listening_lock = threading.Lock()   #ensures that routers_listening does not encounter race conditions

    next_scheduler: [threading.Event] = [] #when the number of routers are known, will store n events to wake up the next router

    def __init__(self, id: int, neighbors: list):
        self.id = id
        self.create_DVM(neighbors)

        threading.Thread(target=Router.host_server, args=[self]).start()

        Router.all_listening.wait()
        self.populate_clients(neighbors)

        self.enforce_order()
        self.old_DVM = self.current_DVM

        round_n = 1 #note -- should be incremented and tracked as a global!!
        print(f"Round {round_n}: {self.id}")
        if self.updated:
            for client_id in self.clients.keys():
                client = self.clients[client_id]
                print(f"Sending DV to node {client_id}")
                msg = bytes("update," + str(self.id) + "," + " ".join(list(map(str, self.current_DVM[self.id]))), encoding='utf-8') #convert id and each elem of dvm into str, cast to bytes with utf-8!
                client.sendall(msg)
                data = client.recv(1024)

        self.updated = False
        self.relax_order()

    #anything put between these two functions will ensure that they happen in a round-robin fashion according to self.id
    def enforce_order(self):
        Router.next_scheduler[self.id].wait()

    def relax_order(self):
        Router.next_scheduler[self.id].clear()
        Router.next_scheduler[(self.id + 1) % Router.num_routers].set()
        
    def create_DVM(self, neighbors):
        N = Router.num_routers
        DVM = [[999]*N for i in range(N)]

        for i in range(N):
            DVM[i][i] = 0

        self.old_DVM = [row[:] for row in DVM]

        for neighbor,weight in neighbors:
            self.updated = True #novel information found, should be shared next iteration
            DVM[self.id][neighbor] = weight
            DVM[neighbor][self.id] = weight

        self.current_DVM = DVM

    def changes_detected(self, dvm1: list, dvm2: list):
        for i in range(len(dvm1)):
            for j in range(len(dvm1)):
                if dvm1[i][j] != dvm2[i][j]:
                    return True
        return False

    #creates permanent socket connections to other connected routers    
    def populate_clients(self, neighbors):
        self.clients = {}
        for router_id, weight in neighbors:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((socket.gethostname(), 50000+router_id))
            self.clients[router_id] = client

    #maybe maintain 2 versions of DVs, one to be update when new info comes in and another to provide the illusion of synchronized iteration
    #non-blocking listening socket that allows for code to execute at least every quarter second
    def host_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((socket.gethostname(), 50000 + self.id))
        server.listen(10)

        read_list = [server]
        while True:
            readable, writable, errored = select.select(read_list, [], [], 0.25)

            #Add new listening router until all are listening
            Router.listening_lock.acquire()
            if self.id not in Router.routers_listening:
                Router.routers_listening.add(self.id)
                if len(Router.routers_listening) == Router.num_routers: #if all are listening then clients can start connecting to servers
                    Router.all_listening.set()
            Router.listening_lock.release()
            
            for s in readable:
                if s is server:
                    client_socket, address = server.accept()
                    read_list.append(client_socket)
                else:
                    try:
                        data = s.recv(1024)
                    except Exception as data_error:
                        print(f"got data encoding error: {data_error}.\ndata: {data}")
                        continue 
                    if not data: #ACKs should be ignored!
                        continue
                    
                    #now process data message
                    data = data.decode('utf-8')
                    cmd, neighbor_id, neighbor_dv = data.split(',')
                    neighbor_id = int(neighbor_id)
                    neighbor_dv = [int(elem) for elem in neighbor_dv.split(' ')]

                    if cmd == 'update':
                        #DV algorithm!
                        old_dvm = self.current_DVM

                        my_dv = self.current_DVM[self.id]
                        print(f"Node {self.id} received DV from {neighbor_id}")
                        print(f"Updating DV matrix at node {self.id}")
                        for router_id in range(len(my_dv)):
                            if router_id == self.id: continue
                            my_dv[router_id] = min(my_dv[router_id], my_dv[neighbor_id] + neighbor_dv[router_id])
                        self.current_DVM[self.id] = my_dv
                        print(f"New DV matrix at node {self.id}: {self.current_DVM[self.id]}\n")

                        #check whether DVM changed, update 'updated' flag
                        new_dvm = self.current_DVM
                        if self.changes_detected(old_dvm, new_dvm): #TODO: think this is broke!
                            self.updated = True

                        s.send(b"Received!") #don't delete
                    #TODO: write section cmd == 'share' where client shares DV. should use code currently in __init__
                    elif cmd == 'has_updates?':
                        s.sendall(bytes(str(self.updated), encoding='utf-8'))
                    elif cmd == 'end':
                        print(f"Node #{self.id} DV = {self.current_DVM[self.id]}")
                        return
                    else:
                        s.close()
                        read_list.remove(s)