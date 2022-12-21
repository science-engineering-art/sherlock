import numpy as np
import matplotlib
import json
import matplotlib.pyplot as plt
import os

# boolean model evaluation meassures


def plot_eval_meassures(data, path, plot_color):
    P_vs_R = {}

    for key in data:
        if key != "max":
            P_vs_R[data[key]["P"]] = data[key]["R"]

    P_vs_R = sorted(P_vs_R.items(), key=lambda x: x[1])

    x = [P_vs_R[i][1]
         for i in range(0, len(P_vs_R))]  # Recall
    y = [P_vs_R[i][0] for i in range(0, len(P_vs_R))]  # Precision

    fig = plt.figure()
    ax = plt.axes()

    plt.xlabel("Recall")
    plt.ylabel("Precision")
    ax.plot(x, y, color=plot_color)

    fig.savefig(path + "/PR_plot.png")


path = os.getcwd()
path = path.split('/')
path = path[0:len(path)-3]
path = "/".join(path)

models = ["BooleanModel", "VectorModel", "FuzzyModel"]
corpus = [("cranfield", "orange"), ("vaswani", "plum"),
          ("cord19/trec-covid/round1", "turquoise")]

for model in models:
    for corp in corpus:
        if model != "FuzzyModel" and corp[0] != "cord19/trec-covid/round1":
            temp = path + f'/ddb_storage/{model}/{corp[0]}'

            with open(temp + "/k_Rank.json") as json_file:
                data = json.load(json_file)

                plot_eval_meassures(data, temp, corp[1])
