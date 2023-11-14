import time, socket
from socket_utils import start_main_socket, signal_router

class Router:
    def __init__(self, N: int, router_id: int, neighbors: list):
        self.id = 50000+router_id
        self.neighbor_sockets = [] #list of sockets to neighbors

        #initialize the distance-vector matrix for this router. add immediate neighbors
        DVM = [[999]*N for i in range(N)]
        for neighbor,weight in neighbors:
            DVM[router_id][neighbor] = weight
        self.DVM = DVM #this router's distance-vector matrix

        #go into message mode--wait to receive messages from either Main or other routers.
        self.receive()

    def receive(self):
        #now listen for commands from main or other routers
        #set up socket that router will use for duration of experiment
        host, port = '', self.id
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #allows for address/port reuse
        s.bind((host,port))
        s.listen(1)
        conn, addr = s.accept()
        while True:
            try:
                msg = conn.recv(1024)
                msg = str(msg).strip()[2:-1]
                msg = msg.split(": ")
                if msg[0] == "close":
                    break
                elif msg[0] == "share_table":
                    self.share(conn)
                elif msg[0] == "update_table":
                    self.update(conn, msg[1])
                else:
                    msg = "(router #"+ str(self.id)+") could not interpret your message of: " + msg
                    conn.sendall(bytes(msg, "utf-8"))
            except Exception as e:
                msg = "(router #"+ str(self.id)+") had exception: " + e
                conn.sendall(bytes(msg, "utf-8"))

    def update(self, conn: socket.socket, payload: str):
        #TODO: the DV algorithm should be implemented here! 
        msg = "(router #"+ str(self.id)+") updated successfully. payload: " + payload
        conn.sendall(bytes(msg, "utf-8"))

    def share(self, conn: socket.socket):
        #TODO: the router should send its DV to relevant neighbor(s) here, if it has updates to share.
        self.DVM_updated = True #NOTE: this should be set during self.update() above
        if self.DVM_updated:
            neighbor_ids = []
            for neighbor_router in range(len(self.DVM)):
                neighbor_id = 50000+neighbor_router
                if neighbor_id == self.id: continue #don't need to send ourselves updates
                #DV_to_share = self.DVM[neighbor_router]
                #prepare DV_to_share as string
                #create socket to neighbor (can I reuse my functions from socket_utils?)
                #s = start_main_socket(neighbor_router)
                #response = signal_router(s, "update_table: HELLO SEAN, YOUR EVIL PLAN WORKED!")
                #s.close()
                #send DV_to_share through socket
                neighbor_ids.append(str(neighbor_id))
            
            msg = "(router #"+ str(self.id)+") shared with neighbors (routers #" + ', #'.join(neighbor_ids) + ") successfully."
            conn.sendall(bytes(msg, "utf-8"))
        else:
            msg = "(router #"+ str(self.id)+") didn't have updates."
            conn.sendall(bytes(msg, "utf-8"))