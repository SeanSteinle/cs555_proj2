import time, socket

class Router:
    def __init__(self, N: int, router_id: int, neighbors: list):
        self.id = 50000+router_id

        #initialize the distance-vector matrix for this router. add immediate neighbors
        DVM = [[999]*N for i in range(N)]

        for i in range(N):
            DVM[i][i] = 0

        for neighbor,weight in neighbors:
            DVM[router_id][neighbor] = weight
            DVM[neighbor][router_id] = weight
        self.DVM = DVM #this router's distance-vector matrix
        print(f"DVM created! {self.DVM}")

        #go into message mode--wait to receive messages from either Main or other routers.
        self.receive()

    def receive(self):
        #set up socket that router will use for duration of experiment
        host, port = '', self.id
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #allows for address/port reuse
        s.bind((host,port))
        s.listen(1)
        conn, addr = s.accept()

        #now listen for commands from main or other routers
        while True:
            try:
                msg = conn.recv(1024)
                msg = str(msg).strip()[2:-1]
                msg = msg.split(": ")
                if not msg:
                    break
                elif msg[0] == "share_table":
                    self.share(conn)
                elif msg[0] == "update_table":
                    self.update(conn, msg[1])
                else:
                    msg = "(router #"+ str(self.id)+") could not interpret your message of: " + msg
                    conn.sendall(bytes(msg, "utf-8"))
            except:
                break

    def update(self, conn: socket.socket, payload: str):
        payload = [2, 999, 5, 10, 999]
        sender_id = 1

        for router_id in range(len(self.DVM)):
            for i in range(len(self.DVM[router_id])):
                known_cost = self.DVM[router_id][i]
                new_cost = self.DVM[router_id][sender_id] + payload[i]

                if known_cost <= new_cost:
                    min = known_cost
                else:
                    #new best path found
                    min = new_cost
                    self.DVM_updated = True
                    
                self.DVM[router_id][i] = min
        
        print(f"updated table {self.id} {self.DVM}")

        #TODO: the DV algorithm should be implemented here! 
        msg = "(router #"+ str(self.id)+") updated successfully. payload: " + payload
        conn.sendall(bytes(msg, "utf-8"))

    def share(self, conn: socket.socket):
        #TODO: the router should send its DV to relevant neighbor(s) here, if it has updates to share.
        self.DVM_updated = True #NOTE: this should be set during self.update() above
        if self.DVM_updated:
            for neighbor_router in range(len(self.DVM)):
                if neighbor_router == self.id: continue #don't need to send ourselves updates
                DV_to_share = self.DVM[neighbor_router]
                #prepare DV_to_share as string
                #create socket to neighbor (can I reuse my functions from socket_utils?)
                #send DV_to_share through socket
            msg = "(router #"+ str(self.id)+") shared with neighbors successfully."
            conn.sendall(bytes(msg, "utf-8"))
        else:
            msg = "(router #"+ str(self.id)+") didn't have updates."
            conn.sendall(bytes(msg, "utf-8"))