import sys
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
    print("Data file not supplied.")
    print("Usage: python plot.py {data-file.txt}")
    sys.exit()

filename = sys.argv[1]

data = []
with open(filename, 'r') as file:
    header = file.readline()  # Read the header
    for line in file:
        if line.startswith('#'):
            continue  # Skip comments

        values = line.strip().split()
        if len(values) == 0 or not values[0].isdigit():
            continue  # Skip lines that don't start with a digit

        data.append(list(map(float, values)))

data = list(zip(*data))

# Plotting
fig, axs = plt.subplots(3, 1, figsize=(10, 15), sharex=True)
fig.suptitle(filename, fontsize=14)

axs[0].plot(data[0], data[1], label="Edge-Cut", color="#1a9850", linewidth=1.5)
axs[0].set_ylabel("Edge Cut")

axs[1].plot(data[0], data[2], label="Swaps", color="black", linewidth=1.5)
axs[1].set_ylabel("Swaps")

axs[2].plot(data[0], data[3], label="Migrations", color="brown", linewidth=1.5)
axs[2].set_ylabel("Migrations")
axs[2].set_xlabel("Rounds")

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
