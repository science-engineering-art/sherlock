from numpy import *
import math
import matplotlib.pyplot as plt
from sympy import im
import sys
import dictdatabase as ddb

# t = linspace(0, 2*math.pi, 400)
# a = sin(t)
# b = cos(t)
# c = a + b

# plt.plot(t, a, 'r') # plotting t, a separately 
# plt.plot(t, b, 'b') # plotting t, b separately 
# plt.plot(t, c, 'g') # plotting t, c separately 
# plt.show()

import numpy as np
import matplotlib
import json
import matplotlib.pyplot as plt
import os


def plot_eval_meassures(data, path, plot_color):

    fig = plt.figure()
    ax = plt.axes()

    plt.xlabel("Recall")
    plt.ylabel("Precision")

    for i in range(0,len(data)):
        P_vs_R = {}

        for key in data[i]:
            if key != "max":
                P_vs_R[data[i][key]["P"]] = data[i][key]["R"]

        P_vs_R = sorted(P_vs_R.items(), key=lambda x: x[1])

        x = [P_vs_R[i][1]
             for i in range(0, len(P_vs_R))]  # Recall
        y = [P_vs_R[i][0] for i in range(0, len(P_vs_R))]  # Precision

        
        ax.plot(x, y, color=plot_color[i])

    if sys.platform.startswith('win'):
        fig.savefig(path[0] + "\PR_plot.png")
    elif sys.platform.startswith('linux'):
        fig.savefig(path[0] + "/PR_plot.png")

path = os.getcwd()

models = ["BooleanModel", "VectorModel", "FuzzyModel"]
corpus = [("cranfield", "orange"), ("vaswani", "plum"), 
          ("cord19\\trec-covid\\round1", "turquoise") if sys.platform.startswith('win') else ("cord19/trec-covid/round1", "turquoise")]

for model in models:
    data_list = []
    path_list = []
    for corp in corpus:
        if sys.platform.startswith('linux'):
            if model != "FuzzyModel" or corp[0] != "cord19/trec-covid/round1":
                temp = path.removesuffix("/src") + f'/ddb_storage/{model}/{corp[0]}'
                path_list.append(temp)
                
                with open(temp + "/k_Rank.json") as json_file:
                    data = json.load(json_file)
                    data_list.append(data)
        elif sys.platform.startswith('win'):
            if model != "FuzzyModel" or corp[0] != "cord19\\trec-covid\\round1":
                temp = path.removesuffix("\src") + f'\ddb_storage\{model}\{corp[0]}'
                path_list.append(temp)
                
                with open(temp + "\k_Rank.json") as json_file:
                    data = json.load(json_file)
                    data_list.append(data)    
    plot_eval_meassures(data_list, path_list, [corpus[0][1], corpus[1][1], corpus[2][1]])        

# path1 = path + f'/ddb_storage/VectorModel/{corpus[0][0]}'

# with open(path1 + "/k_Rank.json") as json_file:
#     data1 = json.load(json_file)

# path2 = path + f'/ddb_storage/VectorModel/{corpus[1][0]}'

# with open(path2 + "/k_Rank.json") as json_file:
#     data2 = json.load(json_file)

# path3 = path + f'/ddb_storage/VectorModel/{corpus[2][0]}'

# with open(path3 + "/k_Rank.json") as json_file:
#     data3 = json.load(json_file)

# plot_eval_meassures([data1, data2, data3], [path1, path2, path3], [corpus[0][1], corpus[1][1], corpus[2][1]])