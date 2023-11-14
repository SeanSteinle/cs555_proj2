import threading
from router import Router

def network_init(filename: str):
    neighbors_dict = read_nodes(filename)
    threads = spinup_threads(neighbors_dict)
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

def spinup_threads(neighbors_dict: dict): #network_map is NxN array
    #using this to learn about threads: https://realpython.com/intro-to-python-threading/
    Router.start_routers(neighbors_dict.keys, )

    for router_id in neighbors_dict.keys():
        thread = threading.Thread(target=Router, args=(len(neighbors_dict.keys()), router_id, neighbors_dict[router_id]))
        threads.append(thread)

    return threads