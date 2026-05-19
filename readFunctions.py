import tkinter.messagebox
import numpy as np
import pandas as pd
from compositeScore import  calcCompositeScore
from tkinter import *
from numpy.f2py.auxfuncs import l_and
from scrollableFrame import ScrollableFrame


def readMetadata():
    try:
        df = pd.read_csv("courses_1115515.csv", delimiter=',')
        rows,cols= df.shape
        if (rows < 1):
            tkinter.messagebox.showerror("Error", "File not having contents/Improper file")
            return

        window = Tk("Metadata")
        window.title("Courses Metadata")

        window.geometry("1280x720")
        frame = ScrollableFrame(window)
        # adding all the other rows into the grid
        column_names= df.columns
        i=0
        for j, col in enumerate(column_names):
            text = Text(frame.scrollable_frame, width=25, height=1, bg="#9BC2E6")
            text.grid(row=i, column=j)
            text.insert(INSERT, col)
        for i in range(rows):
            for j in range(cols):
                text = Text(frame.scrollable_frame, width=25, height=3)
                text.grid(row=i + 1, column=j)

                text.insert(INSERT, df.values[i][j])
        frame.pack(fill='both')
        window.configure(width=rows * 25)
        window.mainloop()
    except:
        tkinter.messagebox.showerror("Error", "File not having contents/Improper file")
        print("Error occured")



def readFromCSVWithFilters(maxCost,language,category,difficulty,subjectNames,dropdownMenu):
    try:
        df = pd.read_csv("courses_1115515.csv", delimiter=',')
        resDf = pd.DataFrame(columns=["Title", "Price (in $)", "Difficulty","Subject Category","Provider","Course Length (in Days)","Course Language"])
        rows, cols = df.shape
        if(rows<1):
            tkinter.messagebox.showerror("Error", "File not having contents/Improper file")
            return
        else:
            tkinter.messagebox.showinfo("Filters applied", "File saved successfully!")

        # adding all the other rows into the grid
        column_names = df.columns
        i = 0
        dropdownMenu["menu"].delete(0, "end")
        for i in range(rows):
            for j in range(cols):

                diffComp = (df.values[i][2].lower() == difficulty.lower() or difficulty == '')
                categoryComp = (df.values[i][3].lower() == category.lower() or category == '')
                maxCostComp = (maxCost == '' or df.values[i][1] <= float(maxCost))
                langComp = (df.values[i][5].lower() == language.lower() or language == '')
                if (diffComp and categoryComp and maxCostComp and langComp):

                    if(j==0):
                        # need to update menu

                        resDf.loc[resDf.shape[0]]= df.loc[i]

        if(resDf.shape[0]<1):
            tkinter.messagebox.showerror("Error", "No data found with these criteria!")
            return
        else:
            resDf.to_csv("filtered.csv", index=False)
            calcCompositeScore()

    except Exception as E:
        tkinter.messagebox.showerror("Error",  E)
        print(E)