from typing import Any
import numpy as np
from scipy.sparse import coo_matrix
from scipy.linalg import eigh
import matplotlib.pyplot as plt
import networkx as nx


class Graph:

    def __init__(self):
        self.filename = None
        self.E = None
        self.edges = []
        self.nodes = []
        self.A = None
        self.D = None
        self.L = None
        self.max_ids = None
        self.eigenvalues = None
        self.G = None
        self.pos = None
        self.cluster_labels = None
        self.number_of_clusters = None

    def load_data(self):
        self.E = np.loadtxt(self.filename, delimiter=',')
        self.edges = [tuple(int(y) for y in x) for x in self.E]
        self.nodes = np.unique(np.asanyarray(self.edges))

    def create_L_matrix(self): # Laplacian Matrix
        self.D = np.diag(np.sum(self.A, axis=1))
        D_inv = np.linalg.inv(self.D)
        self.L = np.dot(np.dot(D_inv, self.A), D_inv)


    def visualize_graph(self):
        self.G = nx.from_numpy_array(self.A)
        self.G.add_nodes_from(self.nodes)
        self.G.add_edges_from(self.edges)
        self.pos = nx.spring_layout(self.G, k=0.1, iterations=35)
        nx.draw(self.G,node_size=15, pos=self.pos, node_color=self.cluster_labels)
        plt.title('Graph Visualization')
        plt.show()

    def __call__(self, filename):
        self.filename = filename
        self.load_data()
