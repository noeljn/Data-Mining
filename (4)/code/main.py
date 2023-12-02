import numpy as np
from scipy.sparse import coo_matrix
from scipy.linalg import eigh
import matplotlib.pyplot as plt
import networkx as nx
from classes import Graph
from sklearn.cluster import KMeans

# Create a graph object
G = nx.read_edgelist('data/example1.dat', delimiter=',')
nx.draw(G, node_size=15)
plt.show()

def spectral_clustering(G):
    A = nx.adjacency_matrix(G)
    D = np.diagflat(np.sum(A, axis=1))
    D_inv = np.linalg.inv(D)
    L = np.dot(np.dot(D_inv, A), D_inv)

    eigenvalues, v = eigh(L)

    # Get the k largest eigenvectors
    k = np.ediff1d(eigenvalues).argmax() + 1
    print(k)
    X = v[:, -k:]
    Y = X / np.linalg.norm(X, axis=1, keepdims=True)
    kmeans = KMeans(n_clusters=k, random_state=0).fit(Y)

    _, fiedler_vector = eigh(D-A)
    fiedler_vector = fiedler_vector[:, 1]

    return kmeans.labels_, fiedler_vector, A

#labels, fiedler_vector, A = spectral_clustering(G)
G = Graph()

G(filename='data/example1.dat')

#G.visualize_graph()
#
G.number_of_clusters = 4

# Step 1. Construct the affinity matrix
#G.max_ids = np.max(G.nodes)
#G.A = np.zeros((G.max_ids, G.max_ids))
print(len(G.edges))
print(G.number_of_nodes())
print(G.number_of_edges())
for x in G.edges:
    print(x)
gamma = 1 # some constant - TODO: update this later!
for i, edge in enumerate(G.edges): # Iterate over the edges
    for j in range (len(G.edges)): #

        pairwise_similarity = np.exp((-abs(G[i] - G[j]))**2) / (2 * gamma**2)
        G.A[i][j] = pairwise_similarity
    
    #G.A[edge[0]-1, edge[1]-1] = 1

# Create the affinity matrix. Holds the pairwise similarity between nodes using a Gaussian kernel.
gamma = 1 # some constant - update this later!
#for np.exp(-abs(G[i] -))

#affinity_matrix = np.exp(-gamma * G.A)
#affinity_matrix = np.exp(-gamma * np.square(np.linalg.norm(G[:, None] - G, axis=2)))

# Construct the diagonal matrix
G.D = np.diag(np.sum(G.A, axis=1))
D_inv = np.linalg.inv(G.D)
G.L = np.dot(np.dot(D_inv, G.A), D_inv)

# Plot the eigenvalues
G.eigenvalues, v = eigh(G.L)
plt.plot(G.eigenvalues)
plt.title('Eigenvalues')
#plt.show()

# Get the k largest eigenvectors
# Sort the eigenvalues in ascending order
idx = G.eigenvalues.argsort()
k = G.number_of_clusters
X = v[:, idx[0:k]]
print(X.shape)

# Renormalize the eigenvectors to have unit length 
Y = np.zeros(X.shape)
for i in range(X.shape[1]):
    Y[:, i] = X[:, i] / np.linalg.norm(X[:, i])
    

# Cluster the data using k-means
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=k, random_state=0).fit(Y)
G.cluster_labels = kmeans.labels_

# Visualize the graph
G.visualize_graph()

"""
It creates a sparse matrix As with dimensions max_ids x max_ids.
 The matrix is populated with 1’s at the locations specified by the vectors col1 and col2. 
 The remaining elements of the matrix are 0’s.
"""

