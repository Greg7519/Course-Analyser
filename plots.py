import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.pyplot import xlabel, title
from pandas.plotting._matplotlib import BarPlot

"""
Υλοποιήθηκαν 3 γραφήματα αξιοποιώντας τη βιβλιοθήκη matplotlib
Αυτά ήταν pie, bar, καθώς και line chart
Οι δυσκολίες που αντιμετωπίστηκαν ήταν η ανάγκη αφαίρεσης δυσκολίων που αντιστοιχούσαν σε 0 μαθήματα,
καθώς έκαναν το γράφημα μη αναγνώσιμο.Επίσης στο pie διάγραμμα λόγω της μη παροχής επίπεδου δυσκολίας
απο το api έπρεπε να προσθέσουμε και τα μαθήματα με άγνωστη δυσκολία
"""


def LinePlot():
    df = pd.read_csv("courses_1115515.csv", delimiter=',')
    df = df.sort_values(by="Course Length (in Days)", ascending=False)
    df = df.head(5)

    # Ταξινόμηση από το μικρότερο στο μεγαλύτερο για τη γραμμή
    df = df.sort_values(by="Course Length (in Days)", ascending=True)

    x = df["Course Length (in Days)"]
    y = df["Price (in $)"]

    # Σχεδίαση της βασικής μαύρης γραμμής
    plt.plot(x, y, color="black", zorder=1)

    # Χρώματα για να ξεχωρίζουν τα μαθήματα (μην τυχών κι το ένα πέσει πάνω στο άλλο)
    chromata = ['blue', 'green', 'orange', 'purple', 'red']


    plt.plot(x.iloc[0], y.iloc[0], marker='o', color=chromata[0], markersize=10,
             label=f"Price: {y.iloc[0]}$, Days: {x.iloc[0]}")
    plt.plot(x.iloc[1], y.iloc[1], marker='o', color=chromata[1], markersize=8,
             label=f"Price: {y.iloc[1]}$, Days: {x.iloc[1]}")
    plt.plot(x.iloc[2], y.iloc[2], marker='o', color=chromata[2], markersize=6,
             label=f"Price: {y.iloc[2]}$, Days: {x.iloc[2]}")
    plt.plot(x.iloc[3], y.iloc[3], marker='o', color=chromata[3], markersize=4,
             label=f"Price: {y.iloc[3]}$, Days: {x.iloc[3]}")
    plt.plot(x.iloc[4], y.iloc[4], marker='o', color=chromata[4], markersize=2,
             label=f"Price: {y.iloc[4]}$, Days: {x.iloc[4]}")

    plt.grid(True)
    plt.xlabel("Course Length (in Days)")
    plt.ylabel("Price (in $)")
    plt.title("Line Plot with Grid")

    # Legend με τιμή και χρόνο
    plt.legend(loc="upper center")

    plt.savefig("LinePlot.png")
    plt.show()


def PieChart():
    df = pd.read_csv("courses_1115515.csv", delimiter=',')
    diffCol = df.get("Difficulty")

    data = [0, 0, 0, 0]
    for col in diffCol:
        if col == "beginner":
            data[0] += 1
        if col == "intermediate":
            data[1] += 1
        if col == "advanced":
            data[2] += 1
        if col == "unknown":
            data[3] += 1


    label1 = "Beginner: " + str(data[0])
    label2 = "Intermediate: " + str(data[1])
    label3 = "Advanced: " + str(data[2])
    label4 = "Unknown: " + str(data[3])

    my_labels = [label1, label2, label3, label4]
    plt.figure(figsize=(10, 7))
    plt.title("Courses based on difficulty")
    myexplode = [0.1, 0, 0, 0]
    plt.pie(data, explode=myexplode, shadow=True)

    plt.legend(title="Difficulties",labels=my_labels)
    plt.savefig("PieChart.png")
    plt.show()

def BarChart():
    matplotlib.rcParams.update({'figure.autolayout': True})
    df = pd.read_csv("courses_1115515.csv", delimiter=',')
    dfSorted= df.sort_values(by= "Course Length (in Days)" , ascending=False)


    top5=dfSorted.head(5)


    names = top5["Title"]
    values = top5["Course Length (in Days)"]
    cols=len(names)

    fig = plt.figure(figsize=(15, 8))
    bars=plt.bar(range(cols),values, width=0.4, color="#4CAF50")
    plt.xticks(range(cols), names, rotation=90)
    plt.bar_label(bars)

    #Αντί για διάρκεια σε ώρες, το κάναμε διάρκεια σε ημέρες επειδή η πληθώρα μαθημάτων (όλα για την ακρίβεια) είχαν τον χρόνο
    # μαθημάτων σε ημέρες,εβδομάδες, μήνες
    plt.ylabel('Course Length (in Days)', fontsize = 12.5)
    plt.tick_params(axis='x',rotation=90,labelsize=12.5)
    plt.tick_params(axis='y', labelsize=12.5)
    plt.savefig("BarChart.png")
    plt.show()