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

    # def start_router(id: int, ):
    #     Router.num_routers += 1
    #     t = threading.Thread(target=Router, args=[id])
    #     t.start()

    def __init__(self, id: int, neighbors: list):
        self.id = id
        self.create_DVM(neighbors)

        threading.Thread(target=Router.host_server, args=[self]).start()

        Router.all_listening.wait()
        self.populate_clients(neighbors)

        # while True: #TODO: print better and end when converged
        self.enforce_order()
        print(f"Current DV matrix: {self.current_DVM}")
        print(f"Last DV matrix: {self.old_DVM}")
        update_string = "Updated" if self.updated else "Not Updated" #all routers are initially set to 'updated'
        print(f"Updated from last DV matrix or the same? {update_string}")
        self.old_DVM = self.current_DVM

        if self.updated:
            for client_id in self.clients.keys():
                client = self.clients[client_id]
                msg = bytes("update," + str(self.id) + "," + " ".join(list(map(str, self.current_DVM[self.id]))), encoding='utf-8') #convert id and each elem of dvm into str, cast to bytes with utf-8!
                client.sendall(msg)
                # client.sendall(f"Hello #{client_id} from router {self.id}!!!".encode())
                data = client.recv(1024)
            # print(f"Received from server: {data.decode()}")

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
                print(f"Routers listening: {Router.routers_listening}")
                if len(Router.routers_listening) == Router.num_routers: #if all are listening then clients can start connecting to servers
                    Router.all_listening.set()
            Router.listening_lock.release()
            
            for s in readable:
                if s is server:
                    client_socket, address = server.accept()
                    read_list.append(client_socket)
                    # print("Connection from", address)
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
                    cmd, sender_id, dv = data.split(',')
                    dv = [int(elem) for elem in dv.split(' ')]

                    if cmd == 'update':
                        print(f"Router {self.id} received {dv} from {sender_id}") #TODO: now update dvm using dv
                        #TODO: now we need to implement the DV algorithm here
                        old_dvm = self.current_DVM

                        #~rest of algorithm goes here~

                        new_dvm = self.current_DVM
                        if self.changes_detected(old_dvm, new_dvm):
                            self.updated = True

                        # print(f"Router #{self.id} received {data.decode()}")
                        s.send(b"Received!")
                    elif cmd == 'has_updates?':
                        s.sendall(bytes(str(self.updated), encoding='utf-8'))
                    elif cmd == 'end':
                        return
                    else:
                        s.close()
                        read_list.remove(s)