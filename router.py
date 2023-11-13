import time, socket

class Router:
    def __init__(self, N: int, router_id: int, neighbors: list):
        self.id = 50000+router_id

        #initialize the distance-vector matrix for this router. add immediate neighbors
        DVM = [[999]*N for i in range(N)]
        for neighbor,weight in neighbors:
            DVM[router_id][neighbor] = weight
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
        #if message is from Main, send()
        #if message is from another router, update()

    def update(self, conn, data):
        #print(f"showing data from router #{self.id}: {data}")

        #TODO: the DV algorithm should be implemented here! 
        msg = "(router #"+ str(self.id)+") updated successfully. data is " + data
        conn.sendall(bytes(msg, "utf-8"))

    def share(self, conn):
        msg = "(router #"+ str(self.id)+") shared successfully."
        conn.sendall(bytes(msg, "utf-8"))

    def close(self, conn, s):
        msg = "(router #"+ str(self.id)+") connection closed."
        conn.sendall(bytes(msg, "utf-8"))
        s.close()