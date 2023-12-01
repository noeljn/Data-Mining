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
        


def calculate_metrics(predictions, ground_truth):
    # Calculate Mean Absolute Error (MAE)
    mae = sum(abs(predictions - ground_truth)) / len(predictions)

    # Calculate Mean Absolute Percentage Error (MAPE)
    mape = 100 * sum(abs(predictions - ground_truth) / ground_truth) / len(predictions)

    return mae, mape

def plott(path_triest_base, path_triest_impr, ground_truth):
    # Read the first file
    df1 = pd.read_csv(path_triest_base)

    # Read the second file
    df2 = pd.read_csv(path_triest_impr)


    # Assuming you have predicted values from your data
    predictions1 = df1["triangles"]
    predictions2 = df2["triangles"]

    # Plot the first set of data in blue
    plt.scatter(df1["M"], predictions1, label="File 1", color="blue")

    # Plot the second set of data in red
    plt.scatter(df2["M"], predictions2, label="File 2", color="red")

    # Add a ground truth line at y=your_value
    plt.axhline(y=ground_truth, color='green', linestyle='--', label='Ground Truth')

    plt.xlabel("M")
    plt.ylabel("Triangles")
    plt.title("Triest-Baseline vs Triest-Improved")
    
    # Set the desired tick positions
    plt.xticks([1000, 5000, 10000])

    # Show the legend to differentiate between the two datasets and ground truth
    plt.legend()

    # Calculate MAE and MAPE for each file
    mae1, mape1 = calculate_metrics(predictions1, ground_truth)
    mae2, mape2 = calculate_metrics(predictions2, ground_truth)

    print("MAE for Triest Base:", mae1)
    print("MAPE for Triest Base:", mape1)
    print("MAE for Triest Impr:", mae2)
    print("MAPE for Triest Impr:", mape2)

    plt.show()
path_triest_base = "output/triest_base_facebook.csv"
path_triest_impr = "output/triest_impr_facebook.csv"
plott(path_triest_base, path_triest_impr, 1612010)
