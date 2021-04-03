import pandas as pd
import GEOparse
import scipy
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
import re


def generate_hm(df, nome):
    """
    Function to generate headmaps with dendrogram
    """
    # figure size
    fig = plt.figure(figsize=(10, 8))
    # need to change the line width
    # default line width doesn't look good
    matplotlib.rcParams["lines.linewidth"] = 0.5
    # axis to show where this current axis
    # need to be shown
    ax1 = fig.add_axes([0.09, 0.1, 0.2, 0.6])
    # to generate the array the will be passed
    # to dendrogram, mey
    Y = sch.linkage(df, method="centroid")
    # need to make changes in orientation to
    # make it appear in the left
    # default is top
    Z1 = sch.dendrogram(Y, orientation="left")
    # removing x and y ticks
    ax1.set_xticks([])
    ax1.set_yticks([])
    # to remove the axis
    ax1.axis("off")

    # top side dendogram
    ax2 = fig.add_axes([0.3, 0.71, 0.6, 0.2])
    Y = sch.linkage(df.T, method="ward")
    Z2 = sch.dendrogram(Y)
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.axis("off")

    # main heatmap
    axmatrix = fig.add_axes([0.3, 0.1, 0.6, 0.6])
    # getting the index to get our required values
    # that needs to be shown in the heatmap
    idx1 = Z1["leaves"]
    idx2 = Z2["leaves"]
    D = df.values[idx1, :]
    D = df.values[:, idx2]
    #     D = df.values
    # using matshow to display the heatmap
    # colormap: 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'
    axmatrix.matshow(D, aspect="auto", origin="lower", cmap="seismic")
    axmatrix.set_xticks([])
    axmatrix.set_yticks([])

    # xticks to the right (x-axis)
    axmatrix.set_xticks(range(len(df.columns)))
    # this shows the required labels
    # in this case it is the dataframe columns
    axmatrix.set_xticklabels(df.columns, minor=False)
    axmatrix.xaxis.set_label_position("bottom")
    axmatrix.xaxis.tick_bottom()

    # to change the rotation of xticks
    plt.xticks(rotation=90, fontsize=8)

    # xticks to the right (y-axis)
    axmatrix.set_yticks(range(len(df.index)))
    # this shows the required labels
    # in this case it is the dataframe index
    axmatrix.set_yticklabels(df.index, minor=False)
    axmatrix.yaxis.set_label_position("right")
    axmatrix.yaxis.tick_right()

    plt.savefig(nome)


# n10694 = pd.read_csv("./csv/new10694.csv")
n49012 = pd.read_csv("results_nashonly/miRNA_nash/exp-vals-nash - GSE49012.csv")
n59492 = pd.read_csv("results_nashonly/miRNA_nash/exp-vals-nash - GSE59492.csv")
# n74618 = pd.read_csv("./csv/new74618.csv")

n59492.set_index("ID_REF", drop=True, inplace=True)
n59492.sort_index(axis="columns", inplace=True)
# generate_hm(n59492, nome="hm_n59492.jpg")

n49012.set_index("ID_REF", drop=True, inplace=True)
n49012.sort_index(axis="columns", inplace=True)
n49012x = np.log2(n49012)
generate_hm(n49012x, nome="hm_n49012.jpg")
