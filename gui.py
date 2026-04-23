# This is a sample Python script.
import tkinter as tk
from tkinter import *

root = tk.Tk()
root.geometry("1280x720")
root.title("Counting Seconds")
frame1 = tk.Frame(root, width=500, height=500)
paddingYVal=15
addSubjectsBtn = tk.Button(frame1, text="Προσθήκη μαθημάτων", width=25)
addSubjectsBtn.pack(pady=paddingYVal,side="top")
addSubjectsBtn = tk.Button(frame1, text="Εμφάνιση metadata μαθημάτων", width=25)
addSubjectsBtn.pack(pady=paddingYVal)
# Dropdown options
days = [""]

# Selected option variable
opt = StringVar(value="")

# Dropdown menu
OptionMenu(frame1, opt, *days).pack()
showGraphsBtn= tk.Button(frame1, text=" Εμφάνιση γραφημάτων", width=25)
showGraphsBtn.pack(pady=paddingYVal)
exportsBtn= tk.Button(frame1, text="Εξαγωγή δεδομένων σε CSV", width=25)
exportsBtn.pack(pady=paddingYVal)
listbox = tk.Listbox(frame1)
listbox.pack(pady=paddingYVal)
listbox.pack_forget()
#ebala frame gia na ta exw ola mazi
frame1.pack(pady=(200,200))
root.mainloop()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
