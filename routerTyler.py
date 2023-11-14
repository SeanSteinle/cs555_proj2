import threading
import select
import socket

class Router:

    num_routers = 0

    all_listening = threading.Event()

    routers_listening = set()
    listening_lock = threading.Lock()

    def __init__(self, id: int) -> None:
        self.id = id
        print(f"Router {self.id} created!")

        threading.Thread(target=Router.host_server, args=[self]).start()

        Router.all_listening.wait()
        
        self.edges = {}
        for router_id in Router.routers_listening - {self.id}:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('', 50000+router_id))
            self.edges[router_id] = client
            client.sendall(f"Hello #{router_id} from router {self.id}!!!".encode())
            data = client.recv(1024)
            # print(f"Received from server: {data.decode()}")
            

#maybe maintain 2 versions of DVs, one to be update when new info comes in and refresh the printable one when it is its turn to update
    def host_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('', 50000 + self.id))
        server.listen(10)

        read_list = [server]
        while True:
            readable, writable, errored = select.select(read_list, [], [], 0.25)
            Router.listening_lock.acquire()
            if self.id not in Router.routers_listening:
                Router.routers_listening.add(self.id)
                print(f"Routers listening: {Router.routers_listening}")
                if len(Router.routers_listening) == Router.num_routers:
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
    
    def start_router(id: int):
        Router.num_routers += 1
        t = threading.Thread(target=Router, args=[id])
        t.start()

    def start_n_routers(n: int):
        for i in range(n):
            Router.start_router(i)

