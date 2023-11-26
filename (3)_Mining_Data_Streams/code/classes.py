from typing import Any, Tuple, Callable, Set, DefaultDict, FrozenSet
import random
import time
import networkx as nx
from tqdm import tqdm
import csv
import pandas as pd
import matplotlib.pyplot as plt

class Dataset():

    def __init__(self, path: str):
        print("Reading graph...")
        start = time.time()
        self.path = path
        self.graph_raw = nx.read_edgelist(self.path, comments='#') 
        self.graph_raw.remove_edges_from(nx.selfloop_edges(self.graph_raw))
        self.graph_raw = nx.convert_node_labels_to_integers(self.graph_raw)
        end = time.time()
        print(f"Time to read graph: {end - start}")

    def get_stream(self) -> Any:
        for edge in tqdm(self.graph_raw.edges()):
            yield edge

class TriestBase:

    def __init__(self, M: int):
        self.M = M
        self.t = 0
        self.global_counter = 0 # Global counter of triangles in the sample
        self.local_counters = DefaultDict[int, int](int)
        self.S = set()

    def sample_edge(self, t: int) -> bool:

        # Check if new edge can be inserted
        if t <= self.M: # If the memory M has not been filled yet, then insert the current edge
            return True
        
        # If memory M is full, then compute the probability of picking the current edge 
        # from a pool containing it and all edges in the resevoir (sample).
        # If probability is greater than a random number, replace a random edge in the sample with the current edge.
        elif random.random() <= self.M / t:
            remove_edge = random.choice(list(self.S))
            self.S.remove(remove_edge)
            self.update_counters(lambda x, y: x - y, remove_edge)
            return True
        else:
            return False
        
    def update_counters(self, operator: Callable[[int, int], int], edge: Tuple[int, int]) -> None:
        u, v = edge # Edge is a tuple of two nodes u and v

        # Get neighborhood for u and v, respectively
        neighborhood_u = set(map(lambda x: x[1] if x[0] == u else x[0], filter(lambda x: x[0] == u or x[1] == u, self.S))) 
        neighborhood_v = set(map(lambda x: x[1] if x[0] == v else x[0], filter(lambda x: x[0] == v or x[1] == v, self.S))) 

        # Get neighbors of intersection of u and v, i.e. the nodes that form a triangle with u and v
        neighborhood_u_v = neighborhood_u.intersection(neighborhood_v)

        # Update counters (global and local ones)
        for c in neighborhood_u_v:
            self.global_counter = operator(self.global_counter, 1)
            self.local_counters[u] = operator(self.local_counters[u], 1)
            self.local_counters[v] = operator(self.local_counters[v], 1)
            self.local_counters[c] = operator(self.local_counters[c], 1)

    def compute_xi(self) -> float:
        return max(1, (self.t*(self.t - 1) * (self.t - 2)) / (self.M * (self.M - 1) * (self.M - 2)))
    
    def process_edge(self, edge: Tuple[int, int]) -> None:
        self.t += 1
        if self.sample_edge(self.t):
            self.S.add(edge)
            self.update_counters(lambda x, y: x + y, edge)

    def __call__(self, edge_stream: Any) -> int:
        for edge in edge_stream:
            self.process_edge(edge)
        return self.compute_xi() * self.global_counter
    
class TriestImpr:

    def __init__(self, M: int):
        self.M = M
        self.t = 0
        self.global_counter = 0 # Global counter of triangles in the sample
        self.local_counters = DefaultDict[int, int](int)
        self.S = set()

    def sample_edge(self, t: int) -> bool:
        # Check if new edge can be inserted
        if t <= self.M: # If the memory M has not been filled yet, then insert the current edge
            return True
        
        # If memory M is full, then compute the probability of picking the current edge 
        # from a pool containing it and all edges in the resevoir (sample).
        # If probability is greater than a random number, replace a random edge in the sample with the current edge.
        elif random.random() <= self.M / t:
            remove_edge = random.choice(list(self.S))
            self.S.remove(remove_edge)
            return True
        else:
            return False
        
    def compute_eta(self) -> float:
        return max(1, ((self.t - 1) * (self.t - 2)) / (self.M  * (self.M - 1)))
        
    def update_counters(self, operator: Callable[[int, int], int], edge: Tuple[int, int]) -> None:
        u, v = edge # Edge is a tuple of two nodes u and v

        # Get neighborhood for u and v, respectively
        neighborhood_u = set(map(lambda x: x[1] if x[0] == u else x[0], filter(lambda x: x[0] == u or x[1] == u, self.S))) 
        neighborhood_v = set(map(lambda x: x[1] if x[0] == v else x[0], filter(lambda x: x[0] == v or x[1] == v, self.S))) 

        # Get neighbors of intersection of u and v, i.e. the nodes that form a triangle with u and v
        neighborhood_u_v = neighborhood_u.intersection(neighborhood_v)
        
        # Update counters (global and local ones)
        eta = self.compute_eta()
        for c in neighborhood_u_v:
            self.global_counter += eta
            self.local_counters[u] += eta
            self.local_counters[v] += eta
            self.local_counters[c] += eta

    def process_edge(self, edge: Tuple[int, int]) -> None:
        self.t += 1
        self.update_counters(lambda x, y: x + y, edge)
        if self.sample_edge(self.t):
            self.S.add(edge)
            
    def __call__(self, edge_stream: Any) -> int:
        for edge in edge_stream:
            self.process_edge(edge)
        return self.global_counter

def plot(base_path, impr_path):
    # Read the first file
    df1 = pd.read_csv(base_path)
    # Read the second file
    df2 = pd.read_csv(impr_path)
    # Plot the first set of data in blue
    plt.scatter(df1["M"], df1["triangles"], label="Triest Base", color="blue")
    # Plot the second set of data in red
    plt.scatter(df2["M"], df2["triangles"], label="Triest Impr", color="red")
    plt.xlabel("M")
    plt.ylabel("Triangles")
    plt.title("Triest-Baseline vs Triest-Improved")
    # Set the desired tick positions
    plt.xticks([1000, 5000, 10000])
    # Show the legend to differentiate between the two datasets
    plt.legend()
    plt.show()