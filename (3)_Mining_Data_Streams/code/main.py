from typing import Any, Tuple, Callable, Set, DefaultDict, FrozenSet
import random
import time

class Triest:

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
            self.S.remove(random.choice(list(self.S)))
            return True
        else:
            return False
        
    def update_counters(self, operator: Callable[[int, int], int], edge: Tuple[int, int]) -> None:
        u, v = edge # Edge is a tuple of two nodes u and v

        # Get neighborhood for u and v, respectively
        neighborhood_u = set(map(lambda x: x[1] if x[0] == u else x[0], filter(lambda x: x[0] == u or x[1] == u, self.S))) 
        neighborhood_v = set(map(lambda x: x[1] if x[0] == v else x[0], filter(lambda x: x[0] == v or x[1] == v, self.S))) 

        # Get neighbors of intersection of u and v
        neighborhood_u_v = neighborhood_u.intersection(neighborhood_v)

        # Update counters (global and local ones)
        for c in neighborhood_u_v:
            self.global_counter = operator(self.global_counter, 1)
            self.local_counters[u] = operator(self.local_counters[u], 1)
            self.local_counters[v] = operator(self.local_counters[v], 1)
            self.local_counters[c] = operator(self.local_counters[c], 1)

    def compute_xi(self) -> float:
        return max(1, (self.t*(self.t - 1) * (self.t - 2)) / (self.M * (self.M - 1) * (self.M - 2)))
        
class TriestBase(Triest):

    def __init__(self, M: int):
        super().__init__(M)

    def process_edge(self, edge: Tuple[int, int]) -> None:
        self.t += 1
        if self.sample_edge(self.t):
            self.S.add(edge)
            self.update_counters(lambda x, y: x + y, edge)

    def __call__(self, edge_stream: Any) -> int:
        for edge in edge_stream:
            self.process_edge(edge)
        return self.compute_xi() * self.global_counter

def get_stream(path: str) -> Any:
    with open(path, "r") as f:
        for line in f.readlines():
            yield tuple(map(int, line.split()))

    #with open("data/facebook_combined.txt", "r") as f:
    #    edge_stream = map(lambda x: tuple(map(int, x.split())), f.readlines())

def main():
    M = [5000]
    path = "data/facebook_combined.txt"
    iterations = 1
    estimations = []

    for m in M:
        for i in range(iterations):
            print(f"Running iteration {i} with M = {m}")
            start = time.time()
            triest = TriestBase(m)
            xi = triest(get_stream(path))
            end = time.time()
            estimations.append(tuple((xi, end - start)))
    
    for i in range(len(estimations)):
        print(f"Estimation {i}: {estimations[i]}")
        

    # Read the edge stream from file



if __name__ == "__main__":
    main()