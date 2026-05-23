import tkinter as tk
from readFunctions import readFromCSVWithFilters
# Υλόποιηση φίλτρων μέσω tkinter UI και εφαρμόγης στο παραγόμενο CSV
def filtersWindow(subjectsList,dropdownMenu):
    root = tk.Tk()
    root.title("Εισαγωγή κριτηρίων")
    root.geometry('400x200')
    # TextBox for input
    lbl = tk.Label(root, text="Εισάγετε θεματική ενότητα", padx=10)
    lbl.pack()
    subjectInp = tk.Text(root, height=1, width=40)
    subjectInp.pack()
    text = subjectInp.get("1.0", "end-1c")
    lbl = tk.Label(root, text="Εισάγετε επίπεδο δυσκολίας", padx=10)
    lbl.pack()
    diffLevelInp = tk.Text(root, height=1, width=40)
    diffLevelInp.pack()
    lbl = tk.Label(root, text="Εισάγετε μέγιστο κόστος", padx=10)
    lbl.pack()
    maxCostInp = tk.Text(root, height=1, width=40)
    maxCostInp.pack()
    lbl = tk.Label(root, text="Εισάγετε γλώσσα διδασκαλίας", padx=10)
    lbl.pack()
    langInp = tk.Text(root, height=1, width=40)
    langInp.pack()
    def saveInput():
        subjectInpTxt = subjectInp.get("1.0", "end-1c")
        langInpTxt = langInp.get("1.0", "end-1c")
        maxCostInpTxt = maxCostInp.get("1.0", "end-1c")
        diffLevelInpTxt = diffLevelInp.get("1.0", "end-1c")
        readFromCSVWithFilters(maxCostInpTxt,langInpTxt,subjectInpTxt, diffLevelInpTxt)
        root.destroy()
        
    # Button to print input
    btn = tk.Button(root, text="Εφαρμογή κριτηρίων",command=saveInput)
    btn.pack()

    root.mainloop()