# This is a sample Python script.
import tkinter as tk
from apiCalls import freeUdemyCourse
from readFunctions import readMetadata
from getUserInput import filtersWindow
from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import askyesno

from numpy.ma.core import append

from scraper import *

scraped_data_df = pd.DataFrame()
current_web_scraping_source_index = 0

sources_api = [
    {"name": "Udemy", "url": "https://www.udemy.com/courses/free/"},
]

sources_web_scraping=[
    {"name": "Harvard", "url": "https://pll.harvard.edu/catalog"},
    {"name": "Class Central", "url": "https://www.classcentral.com/collection/top-free-online-courses"}
]
def add_subjectsApi():
    global scraped_data_df,current_web_scraping_source_index
    apiDf = freeUdemyCourse()
    flag = askyesno("Confirm Data Collection",
                    "Are you sure you're ready?")  # ελέγχω αν σίγουρα θέλει να κάνει web scrape ο χρήστης
    source = sources_api[0]
    if flag:
        print(f"[{source['name']}] Status: Starting Data Collection...")
        frames = [scraped_data_df, apiDf]
        if apiDf is not None and not apiDf.empty:
            scraped_data_df = pd.concat(frames)
            print(f"[{source['name']}] Status: Success")
            messagebox.showinfo("Success", f"Συλλέχθηκαν {len(apiDf)} μαθήματα από {source['name']}")

            current_web_scraping_source_index += 1
            listbox.delete(0, tk.END)
            listbox.pack()

            for title in scraped_data_df["Title"]:
                listbox.insert(END, title)



    else:
        print(f"[{source['name']}] Status: Failed")
        messagebox.showerror("Error", "Αποτυχία συλλογής δεδομένων.")

def add_subjects():
    global scraped_data_df, current_web_scraping_source_index

    if(current_web_scraping_source_index>=len(sources_web_scraping)): current_web_scraping_source_index = 0 #προσωρινα το βαζω να τρεχει πολλαπλες φορες πανω στα Harvard, Class Central

    source = sources_web_scraping[current_web_scraping_source_index]

    flag = askyesno("Confirm Data Collection","Are you sure you're ready?") #ελέγχω αν σίγουρα θέλει να κάνει web scrape ο χρήστης

    if flag:
        print(f"[{source['name']}] Status: Starting Data Collection...")
        result_df = Scraper(source['url'], source['name'])

        frames = [scraped_data_df, result_df]
        if result_df is not None and not result_df.empty:
            scraped_data_df = pd.concat(frames)

            scraped_data_df=normalize_data(scraped_data_df)
            print(f"[{source['name']}] Status: Success")
            messagebox.showinfo("Success", f"Συλλέχθηκαν {len(result_df)} μαθήματα από {source['name']}")

            current_web_scraping_source_index +=1
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

    if scraped_data_df.empty:
        messagebox.showwarning("Warning", "Δεν υπάρχουν δεδομένα για εξαγωγή.")
        return

    if flag:
        filename = "courses_1115515.csv"
        scraped_data_df.to_csv(filename, index=False)
        print(f"[System] Status: Export to {filename} Successful")
        messagebox.showinfo("Export Success", f"Τα δεδομένα αποθηκεύτηκαν στο {filename}")



root = tk.Tk()
root.geometry("1280x720")
root.title("Web scraper Python ΑΓΓΕΛΟΠΟΥΛΟΣ ΓΡΗΓΟΡΙΟΣ ΠΑΝΑΓΙΩΤΗΣ 1115514 ΚΟΠΙΤΣΑΣ ΝΙΚΟΛΑΣ 115515")

frame1 = tk.Frame(root, width=500, height=500)
paddingYVal = 10
# ebala frame gia na ta exw ola
frame1.pack(pady=20)
addSubjectsBtn = tk.Button(frame1, text="Προσθήκη μαθημάτων", width=35, command=add_subjectsApi)
addSubjectsBtn.pack(pady=paddingYVal, side="top")

addSubjectsBtn = tk.Button(frame1, text="Εμφάνιση metadata μαθημάτων", width=35, command=readMetadata)
addSubjectsBtn.pack(pady=paddingYVal)
# Dropdown options
days = [""]
# Selected option variable
opt = StringVar(value="")
dropdownMenu = OptionMenu(frame1, opt, *days)
addSubjectsBtn = tk.Button(frame1, text="Επιλογή κριτηρίων", width=25,
                           command=lambda: filtersWindow(days, dropdownMenu))
addSubjectsBtn.pack(pady=paddingYVal)

# Dropdown menu
dropdownMenu.pack(pady=5)

showGraphsBtn = tk.Button(frame1, text=" Εμφάνιση γραφημάτων", width=35)
showGraphsBtn.pack(pady=paddingYVal)

exportsBtn = tk.Button(frame1, text="Εξαγωγή δεδομένων σε CSV", width=35, command=export_data)
exportsBtn.pack(pady=paddingYVal)

listbox = tk.Listbox(frame1, width=100, font=("Calibri", 11))
listbox.pack(pady=20, padx=10)

root.mainloop()