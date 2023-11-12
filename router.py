class Router:
    def __init__(self, N: int, router_id: int, neighbors: list):
        self.id = router_id
        #register socket id with global list (wait on this)

        #initialize the distance-vector matrix for this router. add immediate neighbors
        DVM = [[999]*N for i in range(N)]
        for neighbor,weight in neighbors:
            DVM[router_id][neighbor] = weight
        self.DVM = DVM #this router's distance-vector matrix

    def receive(self):
        pass

    def update(self):
        pass

    def send(self):
        pass