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
    diffLevel = ['easy', 'medium', 'hard', 'unknown']
    df = pd.read_csv("courses_1115515.csv", delimiter=',')
    diffCol = df.get("Difficulty")
    data = [0,0,0,0]
    for col in diffCol:
        if(col=="easy" or col=="Εύκολο"):
            data[0]+=1
        if (col == "medium" or col == "Μέτριο"):
            data[1] += 1
        if (col == "hard" or col == "Δύσκολο"):
            data[2] += 1
        if(col=="unknown"):
            data[3] += 1



    # Creating plot
    fig = plt.figure(figsize=(10, 7))
    plt.title("Μαθήματα ανάλογα με δυσκολία")
    plt.pie(data, labels=diffLevel)
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