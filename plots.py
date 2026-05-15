import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.pyplot import xlabel
from pandas.plotting._matplotlib import BarPlot


def LineChart():
    df = pd.read_csv("courses_1115515.csv", delimiter=',')
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
    diffLevel = ['easy', 'medium', 'hard']
    df = pd.read_csv("courses_1115515.csv", delimiter=',')
    diffCol = df.get("Difficulty")
    data = [0,0,0]
    for col in diffCol:
        if(col=="easy" or col=="Εύκολο"):
            data[0]+=1
        if (col == "medium" or col == "Μέτριο"):
            data[1] += 1
        if (col == "hard" or col == "Δύσκολο"):
            data[2] += 1



    # Creating plot
    fig = plt.figure(figsize=(10, 7))
    plt.title("Μαθήματα ανάλογα με δυσκολία")

    plt.pie(data, labels=diffLevel)

    # show plot
    plt.show()
def barPlot():
    matplotlib.rcParams.update({'figure.autolayout': True})
    df = pd.read_csv("courses_1115515.csv", delimiter=',')
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
LineChart()
PieChart()
barPlot()