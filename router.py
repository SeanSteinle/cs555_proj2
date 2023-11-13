import time, socket, pickle, socket_utils, threading

class Router:

    def __init__(self, N: int, router_id: int, neighbors: list):
        self.port = 50000+router_id
        self.id = router_id

        #initialize the distance-vector matrix for this router. add immediate neighbors
        DVM = [999] * N # Changed this to only contain this router's DV
        for neighbor,weight in neighbors:
            DVM[neighbor] = weight
        self.DVM = DVM #this router's distance-vector matrix
        print(f"DVM created! {self.DVM}")



        #go into message mode--wait to receive messages from either Main or other routers.
        self.receive()

    def receive(self):
        #set up socket that router will use for duration of experiment
        host, port = '', self.port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #allows for address/port reuse
        s.bind((host,port))
        s.listen(1)
        conn, addr = s.accept()

        #only now is the router completely spun up
        # main.counter_lock.acquire()
        # main.routers_up += 1
        # print(f"routers actually up {main.routers_up}")
        # # if self.routers_up == len(self.DVM):
        # #     self.all_routers.release()
        # main.counter_lock.release()

        #now listen for commands from main or other routers
        while True:
            try:
                msg = conn.recv(1024)
                msg = str(msg).strip()[2:-1]
                msg = msg.split(": ")
                if not msg:
                    print("not a str?");
                    break
                elif msg[0] == "share_table":
                    self.share(conn)
                elif msg[0] == "update_table":
                    self.update(conn, msg[1])
                else:
                    msg = "(router #"+ str(self.port)+") could not interpret your message of: " + msg
                    conn.sendall(bytes(msg, "utf-8"))
            except:
                print("exception?")
                break

    def update(self, conn: socket.socket, payload: str):
        #TODO: the DV algorithm should be implemented here! 
        msg = "(router #"+ str(self.port)+") updated successfully. payload: " + payload
        conn.sendall(bytes(msg, "utf-8"))

    def share(self, conn: socket.socket):
        #TODO: the router should send its DV to relevant neighbor(s) here, if it has updates to share.
        self.DVM_updated = True #NOTE: this should be set during self.update() above
        payload = pickle.dumps(self.DVM)
        if self.DVM_updated:
            for neighbor_router in range(len(self.DVM)):
                if neighbor_router == self.id: continue #don't need to send ourselves updates
                # DV_to_share = self.DVM[neighbor_router]
                #create socket to neighbor (can I reuse my functions from socket_utils?)
                # s = socket_utils.create_socket(neighbor_router)
                # socket_utils.signal_router_id(s, f"msg from router {self.id}!!")
                #send DV_to_share through socket
            msg = "(router #"+ str(self.port)+") shared with neighbors successfully."
            conn.sendall(bytes(msg, "utf-8"))
        else:
            msg = "(router #"+ str(self.port)+") didn't have updates."
            conn.sendall(bytes(msg, "utf-8"))