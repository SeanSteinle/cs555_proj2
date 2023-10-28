import threading
from collections import defaultdict

def network_init(filename: str):
    neighbors_dict = read_nodes(filename)
    print(neighbors_dict)
    threads = spinup_threads(neighbors_dict)

def read_nodes(filename: str):
    #read directly from file
    with open(filename, "r") as f:
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
    #target function for thread should be a Router() constructor
    pass