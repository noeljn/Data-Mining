import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
import math

def heat_map(df, title, file_path, normalize=False, cmap="rocket", figsize=(10, 10), n= 20):

    heatmap = np.zeros((n, n))

    for row in df.itertuples():
        heatmap[row.document1, row.document2] = row.value
        heatmap[row.document2, row.document1] = row.value
        heatmap[row.document2, row.document2] = 1

    if normalize:
        heatmap = heatmap / heatmap.max()

    plt.figure(figsize=figsize)

    cmap = sns.color_palette("rocket", as_cmap=True)

    sns.heatmap(heatmap, square=True, norm=LogNorm(), cmap=cmap)

    plt.title(title)
    plt.savefig(file_path, dpi=300)
    plt.show()