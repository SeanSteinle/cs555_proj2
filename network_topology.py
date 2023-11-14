import threading
from router import Router

def network_init(filename: str):
    neighbors_dict = read_nodes(filename)
    threads = start_routers(neighbors_dict)
    return threads

def read_nodes(filename: str):
    #read directly from file
    with open(filename, "r")  as f:
        text = f.readlines()
    DV = [line.strip('\n').split(' ') for line in text]
    assert len(DV) == len(DV[0]) #should be NxN!

    #get list of neighbor triples
    neighbor_trips = []
    for node,distance_vector in enumerate(DV):
        for neighbor,weight in enumerate(distance_vector):
            if weight != '0':
                neighbor_trips.append((node,neighbor,int(weight)))

    #turn neighbor triples into neighbors dictionary
    neighbor_dict = {}
    for neighbor_trip in neighbor_trips:
        src,dst,weight = neighbor_trip
        neighbor_dict.setdefault(src,[]).append((dst,weight))

    return neighbor_dict

def start_routers(neighbors_dict: dict):
    Router.num_routers = len(neighbors_dict.keys())

    Router.next_scheduler = [threading.Event() for i in range(Router.num_routers)]
    Router.next_scheduler[0].set() # Router with id 0 should take action first

    threads = []
    for id in range(Router.num_routers):
        threads.append(threading.Thread(target=Router, args=[id, neighbors_dict[id]]))
    return threads