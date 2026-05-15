import tkinter.messagebox
import numpy as np
import pandas as pd
from tkinter import *
from numpy.f2py.auxfuncs import l_and

from scrollableFrame import ScrollableFrame


def calcCompositeScore():
    try:
        df = pd.read_csv("filtered.csv", delimiter=',')
        rows,cols = df.shape
        Cost = df['Price (in $)']
        duration= df['Course Length (in Days)']

        normalizedCost= np.empty((1,rows))
        normalizedDuration= np.empty((1,rows))
        # prevent null exception
        if((np.max(Cost) - np.min(Cost))==0):
            for i in range(rows):
                normalizedCost[i] = 0.5
        else:
            normalizedCost =(1- (Cost - np.min(Cost)) / (np.max(Cost) - np.min(Cost)))*0.5
        #if max and min is equal then whole data set breaks, so i create it
        if ((np.max(duration) - np.min(duration)) == 0):
            for i in range(rows):
                normalizedDuration[i] = 0.5
        else:
            normalizedDuration = (duration-np.min(duration))/(np.max(duration)-np.min(duration))
        for i in range(rows):
            # if its 0 and max not equal to min
            if(normalizedDuration[i]!=0 and (np.max(duration) - np.min(duration)) != 0 ):
                normalizedDuration[i] = (1-normalizedDuration[i])*0.5
        composite_score= np.add(normalizedCost, normalizedDuration)
        composite_score = np.round(composite_score,2)
        df['Composite Score'] = composite_score
        df.sort_values(by=['Composite Score'], inplace=True)
        df.to_csv("filtered.csv", index=False)

        print(composite_score)

    except:
        print("Error occured")

