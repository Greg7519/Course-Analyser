import tkinter.messagebox
import numpy as np
import pandas as pd
from tkinter import *
from numpy.f2py.auxfuncs import l_and

import readFunctions
from scrollableFrame import ScrollableFrame
# Αλγόριθμος έξυπνων συστάσεων
# Ιδανικό αποτέλεσμα 1
# Κόστος= (1-(κανονικοποιημενη τιμη μέσω εύρεσης μεγίστου, οσο μικρότερο το κόστος τόσο το καλύτερο))*0.5
# Διάρκεια=(1-(κανονικοποιημενη τιμη μέσω εύρεσης μεγίστου, οσο μικρότερη η διάρκεια τόσο το καλύτερο))*0.5
# Αν όμως διάρκεια 0, τότε προσθέτει 0(0 σημάινει οτι λείπει η πληροφορία)
# Σκόρ= 0.6*Κοστος + 0.4*Διάρκεια
# Ο λόγος απόδοσης μεγαλύτερης βαρύτητας στο κόστος, είναι ότι επιστρέφεται πάντα σε αντίθεση
# με τη διάρκεια που είναι 0 μερικες φορες, γεγονός που είναι αδύνατο.
# Ταυτόχρονα, λαμβάνεται μέριμνα ώστε κατα την κανονικοποίηση να δοθεί 0.5(δηλαδή το μισό)
# σε περίπτωση ισότητας μεγίστου και ελαχίστου, δηλαδή αν όλα τα στοιχεία έχουν την ίδια τιμή
# σε κάποιο απο τα 2.
#Η κυριότερη πρόκληση ήταν η κατανόηση του αλγορίθμου καθώς και η εύρεση μέσω του τεσταρίσματος ότι αν έχω ας
#πούμε ένα μάθημα τότε το πρόγραμμα χωρίς τον κατάλληλο χειρισμό, θα κρασάρε
def calcCompositeScore():
    try:
        df = pd.read_csv("filtered.csv", delimiter=',')
        rows,cols = df.shape
        Cost = df['Price (in $)']
        duration= df['Course Length (in Days)']

        normalizedCost= np.zeros(rows)
        normalizedDuration= np.zeros(rows)
        # prevent null exception
        if((np.max(Cost) - np.min(Cost))==0):
            for i in range(rows):
                normalizedCost[i]= 0.6
        else:
            normalizedCost =(1- (Cost - np.min(Cost)) / (np.max(Cost) - np.min(Cost)))*0.6
        #if max and min is equal then whole data set breaks, so i create it
        if ((np.max(duration) - np.min(duration)) == 0):
            for i in range(rows):
                normalizedDuration[i] = 0.4
        else:
            normalizedDuration = (duration-np.min(duration))/(np.max(duration)-np.min(duration))
        for i in range(rows):
            # if its 0 and max not equal to min
            if(normalizedDuration[i]!=0 and (np.max(duration) - np.min(duration)) != 0 ):
                normalizedDuration[i] = (1-normalizedDuration[i])*0.4
        composite_score= np.add(normalizedCost, normalizedDuration)
        composite_score = np.round(composite_score,2)
        df['Composite Score'] = composite_score
        df.sort_values(by=['Composite Score'],ascending=False, inplace=True)
        df.to_csv("filtered.csv", index=False)
        from readFunctions import readTop3Subjects
        readTop3Subjects()



    except Exception as e:
        print("Error occured: ", e)