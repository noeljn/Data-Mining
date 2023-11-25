from classes import *


"""Number of triangles: 8611705.228852853
Time: 263.90398049354553"""
 

def test():
    M = [1000, 5000, 10000]
    path = "data/web-NotreDame.txt"
    dataset = Dataset(path)
    iterations = 5
    estimations = []

    for m in M:
        for i in range(iterations):
            print(f"Running iteration {i} with M = {m}")
            start = time.time()
            triest = TriestImpr(m)
            triangles = triest(dataset.get_stream())
            end = time.time()
            estimations.append((i, m, triangles, end - start))
            
    print(estimations)
    
    with open("data/triest_impr.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["iteration", "M", "triangles", "time"])
        writer.writerows(estimations)
        
test()