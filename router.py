import time, socket

class Router:
    def __init__(self, N: int, router_id: int, neighbors: list):
        self.id = 50000+router_id
        #create socket and register socket id with global list (wait on this)


        #initialize the distance-vector matrix for this router. add immediate neighbors
        DVM = [[999]*N for i in range(N)]
        for neighbor,weight in neighbors:
            DVM[router_id][neighbor] = weight
        self.DVM = DVM #this router's distance-vector matrix
        print(f"DVM created! {self.DVM}")

        #go into message mode--wait to receive messages from either Main or other routers.
        self.receive()

    def receive(self):
        host, port = '', self.id
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host,port))
        s.listen(1) #what does 1 do here?
        conn, addr = s.accept()
        while True:
            try:
                command = conn.recv(1024)
                if command == bytes("share_table", "utf-8"):
                    self.share()
                elif command == bytes("update_table", "utf-8"):
                    self.update()

                
                print(f"(router #{self.id}) got message: {command}")
                
                msg = "success from router #" + str(self.id)
                conn.sendall(bytes(msg, "utf-8"))
            except socket.error:
                break
        #if message is from Main, send()
        #if message is from another router, update()

    def update(self):
        pass

    def share(self):
        pass