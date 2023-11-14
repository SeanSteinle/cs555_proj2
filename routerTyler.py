import threading
import select
import socket

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

    def start_routers(neighbors_dict: dict):
        Router.num_routers = len(neighbors_dict.keys())

        Router.next_scheduler = [threading.Event() for i in range(Router.num_routers)]
        Router.next_scheduler[0].set() # Router with id 0 should take action first

        for id in range(Router.num_routers):
            threading.Thread(target=Router, args=[id, neighbors_dict[id]]).start()  #start a Router at init

    def __init__(self, id: int, neighbors: list):
        self.id = id
        self.create_DVM(neighbors)

        #example of how to use the two functions to enforce order between threads
        self.enforce_order()
        print(f"Router {self.id} created! DVM: {self.current_DVM}")
        self.relax_order()

        threading.Thread(target=Router.host_server, args=[self]).start()

        Router.all_listening.wait()
        self.populate_clients(neighbors)

        # while True:
        self.enforce_order()
        print(f"Current DV matrix: {self.current_DVM}")
        print(f"Last DV matrix: {self.old_DVM}")
        update_string = "Updated" if self.updated else "Not Updated"
        print(f"Updated from last DV matrix or the same? {update_string}")
        self.old_DVM = self.current_DVM

        for client_id in self.clients.keys():
            client = self.clients[client_id]
            client.sendall(f"Hello #{client_id} from router {self.id}!!!".encode())
            data = client.recv(1024)
            # print(f"Received from server: {data.decode()}")
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

    #creates permanent socket connections to other connected routers    
    def populate_clients(self, neighbors):
        self.clients = {}
        for router_id, weight in neighbors:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('', 50000+router_id))
            self.clients[router_id] = client

    #maybe maintain 2 versions of DVs, one to be update when new info comes in and another to provide the illusion of synchronized iteration
    #non-blocking listening socket that allows for code to execute at least every quarter second
    def host_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('', 50000 + self.id))
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
                    data = s.recv(1024)
                    if data:
                        print(f"Router #{self.id} received {data.decode()}")
                        s.send(b"Received!")
                    else:
                        s.close()
                        read_list.remove(s)
