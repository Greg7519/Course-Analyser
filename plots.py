import tkinter.messagebox

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.pyplot import xlabel, pie
from pandas.plotting._matplotlib import BarPlot

df = pd.read_csv("courses_1115515.csv", delimiter=',')
def LineChart():
    global df
    df = df.sort_values(by= "Price (in $)" , ascending=False)
    x = df["Course Length (in Days)"]
    y = df["Price (in $)"]
    plt.plot(x, y)
    plt.grid(True)
    plt.xlabel("Course Length (in Days")
    plt.ylabel("Price (in $)")
    plt.title("Line Plot with Grid")
    plt.show()
def PieChart():
    # Creating dataset

    diffLevel = {'easy': 0, 'medium': 0, 'hard': 0, 'unknown': 0}
    df = pd.read_csv("courses_1115515.csv", delimiter=',')
    diffCol = df.get("Difficulty")

    for col in diffCol:
        if(col=="easy" or col=="Εύκολο"):
            diffLevel["easy"] += 1
        if (col == "medium" or col == "Μέτριο"):
            diffLevel["medium"] += 1
        if (col == "hard" or col == "Δύσκολο"):
            diffLevel["hard"] += 1
        if(col=="unknown"):
            diffLevel["unknown"] += 1
    # if level is unknown check if all are unknown
    if (diffLevel.get("easy")==0):
        del(diffLevel["easy"])
    if (diffLevel.get("medium")==0):
        del(diffLevel["medium"])
    if (diffLevel.get("hard")==0):
        del(diffLevel["hard"])
    if (diffLevel.get("unknown")==0):
        del(diffLevel["unknown"])

    # Creating plot
    fig = plt.figure(figsize=(10, 7))
    plt.title("Μαθήματα ανάλογα με δυσκολία")
    plt.pie(diffLevel.values(), labels=diffLevel.keys())
    plt.legend(title="Difficulty level")
    # show plot
    plt.show()
def barPlot():
    matplotlib.rcParams.update({'figure.autolayout': True})
    global df

    dfSorted= df.sort_values(by= "Course Length (in Days)" , ascending=False)

    rows,cols = dfSorted.shape

    names = dfSorted.head(5)["Title"]
    values = dfSorted.head(5)["Course Length (in Days)"]
    fig = plt.figure(figsize = (19.2,10.8))
    plt.xticks(range(rows))
    plt.subplots_adjust(bottom=0.2)
    plt.bar(names,values, width=0.5)

    plt.ylabel('Διάρκεια(Σε ημέρες)', fontsize = 12.5)
    plt.tick_params(axis='x',rotation=90,labelsize=12.5)
    plt.tick_params(axis='y', labelsize=12.5)
    plt.savefig("filtered.png")
    plt.show()
if(df.shape[0]>0):
    LineChart()
    PieChart()
    barPlot()
else:
    tkinter.messagebox.showwarning("No data found in the csv!")
PieChart()