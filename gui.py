# This is a sample Python script.
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import askyesno

from scraper import *

scraped_data_df = None
current_source_index = 0
sources_api = [
    {"name": "Harvard", "url": "https://pll.harvard.edu/catalog"},
    {"name": "Udemy", "url": "https://www.udemy.com/courses/free/"},
    {"name": "Coursera", "url": "https://www.coursera.org/courses?query=free"}
]

sources_web_scraping=[
    {"name": "Harvard", "url": "https://pll.harvard.edu/catalog"},
    {"name": "Class Central", "url": "https://www.classcentral.com/collection/top-free-online-courses"}
]


def add_subjects():
    global scraped_data_df, current_source_index

    source = sources_web_scraping[current_source_index]


    flag = askyesno("Confirm Data Collection","Are you sure you're ready?") #ελέγχω αν σίγουρα θέλει να κάνει web scrape ο χρήστης

    if flag:
        print(f"[{source['name']}] Status: Starting Data Collection...")
        result_df = HarvardScraper(source['url'])

        if result_df is not None and not result_df.empty:
            scraped_data_df = result_df
            print(f"[{source['name']}] Status: Success")
            messagebox.showinfo("Success", f"Συλλέχθηκαν {len(result_df)} μαθήματα από {source['name']}")
            
            listbox.delete(0, tk.END)
            listbox.pack()

            for title in scraped_data_df["Title"]:
                listbox.insert(END, title)
        else:
            print(f"[{source['name']}] Status: Failed")
            messagebox.showerror("Error", "Αποτυχία συλλογής δεδομένων.")



def export_data():

    global scraped_data_df
    flag = askyesno("Confirm Data Exportation", "Are you sure you're ready?")
    if flag:
        if scraped_data_df is not None:

            filename = "courses_115515.csv"
            scraped_data_df.to_csv(filename, index=False)
            print(f"[System] Status: Export to {filename} Successful")
            messagebox.showinfo("Export Success", f"Τα δεδομένα αποθηκεύτηκαν στο {filename}")
        else:
            messagebox.showwarning("Warning", "Δεν υπάρχουν δεδομένα για εξαγωγή.")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1280x720")
    root.title("Web scraper Python ΑΓΓΕΛΟΠΟΥΛΟΣ ΓΡΗΓΟΡΙΟΣ ΠΑΝΑΓΙΩΤΗΣ 1115514 ΚΟΠΙΤΣΑΣ ΝΙΚΟΛΑΣ 115515")

    frame1 = tk.Frame(root, width=500, height=500)
    paddingYVal = 15

    addSubjectsBtn = tk.Button(frame1, text="Προσθήκη μαθημάτων", width=25, command=add_subjects)
    addSubjectsBtn.pack(pady=paddingYVal, side="top")

    addSubjectsBtn = tk.Button(frame1, text="Εμφάνιση metadata μαθημάτων", width=25)
    addSubjectsBtn.pack(pady=paddingYVal)
    # Dropdown options
    days = [""]

    # Selected option variable
    opt = StringVar(value="")

    # Dropdown menu
    OptionMenu(frame1, opt, *days).pack()

    showGraphsBtn = tk.Button(frame1, text=" Εμφάνιση γραφημάτων", width=25)
    showGraphsBtn.pack(pady=paddingYVal)

    exportsBtn = tk.Button(frame1, text="Εξαγωγή δεδομένων σε CSV", width=25, command=export_data)
    exportsBtn.pack(pady=paddingYVal)

    listbox = tk.Listbox(frame1, width=100, font=("Calibri", 11))


    # ebala frame gia na ta exw ola
    frame1.pack(pady=(200, 200))
    root.mainloop()

