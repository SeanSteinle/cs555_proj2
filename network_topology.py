import threading

def network_init(filename: str):
    network_map = read_nodes(filename)
    threads = spinup_threads(network_map)

def read_nodes(filename: str):
    with open(filename, "r") as f:
        text = f.readlines()
    DV = [line.strip('\n').split(' ') for line in text]
    assert len(DV) == len(DV[0]) #should be NxN!
    neighbor_trips = []
    for node,distance_vector in enumerate(DV):
        for neighbor,weight in enumerate(distance_vector):
            if weight != '0':
                neighbor_trips.append((node,neighbor,int(weight)))
    neighbor_dict = dict.fromkeys(range(len(DV)), [])
    for neighbor_trip in neighbor_trips:
        print(neighbor_trip)
        src,dst,weight = neighbor_trip
        neighbor_dict[src].append((dst,weight))
    #do a little more processing here?
    print(neighbor_dict)
    return neighbor_dict

def spinup_threads(network_map: list): #network_map is NxN array
    #target function for thread should be a Router() constructor
    pass