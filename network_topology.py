import threading

def network_init(filename: str):
    network_map = read_nodes(filename)
    threads = spinup_threads(network_map)

def read_nodes(filename: str):
    with open(filename, "r") as f:
        text = f.readlines()
    DV = [line.strip('\n').split(' ') for line in text]
    assert len(DV) == len(DV[0]) #should be NxN!
    neighbors = dict.fromkeys(range(len(DV)), [])
    print(neighbors)
    for node,distance_vector in enumerate(DV):
        for neighbor,weight in enumerate(distance_vector):
            if weight != '0' and node == :
                print(f"{node}-{neighbor}-{weight}")
                neighbors[node].append((neighbor,weight))
    print(neighbors)
    #do a little more processing here?
    return neighbors

def spinup_threads(network_map: list): #network_map is NxN array
    #target function for thread should be a Router() constructor
    pass