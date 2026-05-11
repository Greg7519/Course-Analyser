import pandas as pd
from tkinter import *
from numpy.f2py.auxfuncs import l_and


def readMetadata():
    try:
        df = pd.read_csv("courses_115515.csv", delimiter=',')
        rows,cols= df.shape
        window = Tk("Metadata")
        window.title("Harvard course metadata")
        window.geometry("1280x720")
        # adding all the other rows into the grid
        column_names= df.columns
        i=0
        for j, col in enumerate(column_names):
            text = Text(window, width=25, height=1, bg="#9BC2E6")
            text.grid(row=i, column=j)
            text.insert(INSERT, col)
        for i in range(rows):
            for j in range(cols):
                text = Text(window, width=25, height=3)
                text.grid(row=i + 1, column=j)

                text.insert(INSERT, df.values[i][j])

        window.mainloop()
    except:
        print("No file found")
        exit()


def readFromCSVWithFilters(maxCost,language,category,difficulty,subjectNames):
    try:
        df = pd.read_csv("courses_115515.csv", delimiter=',')
        rows, cols = df.shape
        window = Tk("Metadata")
        window.title("Harvard course metadata")
        window.geometry("1280x720")
        # adding all the other rows into the grid
        column_names = df.columns
        i = 0

        for j, col in enumerate(column_names):
            text = Text(window, width=25, height=1, bg="#9BC2E6")
            text.grid(row=i, column=j)
            text.insert(INSERT, col)
        for i in range(rows):
            for j in range(cols):
                text = Text(window, width=25, height=3)
                text.grid(row=i + 1, column=j)
                diffComp = (df.values[i][2].lower() == difficulty.lower() or difficulty == '')
                categoryComp = (df.values[i][3].lower() == category.lower() or category == '')
                maxCostComp = (maxCost == '' or df.values[i][1] < float(maxCost))
                langComp = (df.values[i][6].lower() == language.lower() or language == '')
                if (diffComp and categoryComp and maxCostComp and langComp):
                    text.insert(INSERT, df.values[i][j])
                    subjectNames.append(df.values[i][j])

        window.mainloop()
    except:
        print('Error occured!')
        exit()


