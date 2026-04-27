# This is a sample Python script.
import tkinter as tk
from tkinter import *
from tkinter import messagebox

from scraper import *

scraped_data_df = None
current_source_index = 0
sources = [
    {"name": "Harvard", "url": "https://pll.harvard.edu/catalog"},
    {"name": "Udemy", "url": "https://www.udemy.com/courses/free/"},
    {"name": "Coursera", "url": "https://www.coursera.org/"}
]


def add_subjects():
    global scraped_data_df, current_source_index

    source = sources[current_source_index]

    print(f"[{source['name']}] Status: Starting Data Collection...")
    result_df = HarvardScraper(False, source['url'])

    if result_df is not None and not result_df.empty:
        scraped_data_df = result_df
        print(f"[{source['name']}] Status: Success")
        messagebox.showinfo("Success", f"Συλλέχθηκαν {len(result_df)} μαθήματα από {source['name']}")


    else:
        print(f"[{source['name']}] Status: Failed")
        messagebox.showerror("Error", "Αποτυχία συλλογής δεδομένων.")






root = tk.Tk()
root.geometry("1280x720")
root.title("Web scraper Python ΑΓΓΕΛΟΠΟΥΛΟΣ ΓΡΗΓΟΡΙΟΣ ΠΑΝΑΓΙΩΤΗΣ 1115514 ΚΟΠΙΤΣΑΣ ΝΙΚΟΛΑΣ 115515")
frame1 = tk.Frame(root, width=500, height=500)
paddingYVal=15
addSubjectsBtn = tk.Button(frame1, text="Προσθήκη μαθημάτων", width=25, command=add_subjects)
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


#ebala frame gia na ta exw ola
frame1.pack(pady=(200,200))
root.mainloop()

