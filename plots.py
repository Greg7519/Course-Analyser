import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.pyplot import xlabel, title
from pandas.plotting._matplotlib import BarPlot


def LineChart():
    df = pd.read_csv("courses_1115515.csv", delimiter=',')
    df = df.sort_values(by= "Course Length (in Days)")
    x = df["Course Length (in Days)"]
    y = df["Price (in $)"]
    plt.plot(x, y, marker='o', color="#ff4d4d")
    plt.grid(True)
    plt.xlabel("Course Length (in Days)")
    plt.ylabel("Price (in $)")
    plt.title("Line Plot with Grid")
    plt.show()


def PieChart():
    diffLevel = ['beginner', 'intermediate', 'advanced']
    df = pd.read_csv("courses_1115515.csv", delimiter=',')
    diffCol = df.get("Difficulty")

    data = [0, 0, 0]
    for col in diffCol:
        if col == "beginner":
            data[0] += 1
        if col == "intermediate":
            data[1] += 1
        if col == "advanced":
            data[2] += 1


    label1 = "Beginner: " + str(data[0])
    label2 = "Intermediate: " + str(data[1])
    label3 = "Advanced: " + str(data[2])

    my_labels = [label1, label2, label3]
    plt.figure(figsize=(10, 7))
    plt.title("Μαθήματα ανάλογα με δυσκολία")
    myexplode = [0.1, 0, 0]
    plt.pie(data, explode=myexplode, shadow=True)

    plt.legend(title="Difficulties",labels=my_labels)

    plt.show()

def BarPlot():
    matplotlib.rcParams.update({'figure.autolayout': True})
    df = pd.read_csv("courses_1115515.csv", delimiter=',')
    dfSorted= df.sort_values(by= "Course Length (in Days)" , ascending=False)


    top5=dfSorted.head(5)


    names = top5["Title"]
    values = top5["Course Length (in Days)"]
    cols=len(names)

    fig = plt.figure()
    bars=plt.bar(range(cols),values, width=0.4, color="#4CAF50")
    plt.xticks(range(cols), names, rotation=90)
    plt.bar_label(bars)

    #Αντί για διάρκεια σε ώρες, το κάναμε διάρκεια σε ημέρες επειδή η πληθώρα μαθημάτων (όλα για την ακρίβεια) είχαν τον χρόνο
    # μαθημάτων σε ημέρες,εβδομάδες, μήνες
    plt.ylabel('Διάρκεια (Σε ημέρες)', fontsize = 12.5)
    plt.tick_params(axis='x',rotation=90,labelsize=12.5)
    plt.tick_params(axis='y', labelsize=12.5)
    plt.savefig("filtered.png")
    plt.show()

LineChart()
PieChart()
BarPlot()