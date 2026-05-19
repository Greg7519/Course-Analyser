# This is a sample Python script.
import tkinter as tk
from readFunctions import readMetadata
from applyFilters import filtersWindow
from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import askyesno
from apiCalls import *
from plots import *

from numpy.ma.core import append, size

from scraper import *


Data_df = pd.DataFrame()
current_web_scraping_source_index = 0


sources_web_scraping=[
    {"name": "Harvard", "url": "https://pll.harvard.edu/catalog"},
    {"name": "Class Central", "url": "https://www.classcentral.com/collection/top-free-online-courses"},
    # στο Coursera εχουμε βαλει να εχουμε συγκεκριμενα αποτελεσματα για πιο ευκολο
    # webscaping αφαιρωντας επιλογες οπως difficulty=mixed, language != English etc
    {"name": "Coursera", "url": "https://www.coursera.org/search?query=web%20development&language=English&productDifficultyLevel=Beginner&productDifficultyLevel=Intermediate&productDifficultyLevel=Advanced&productTypeDescription=Courses&topic=Computer%20Science&sortBy=BEST_MATCH"}
]

def show_graphs():
    BarChart()
    PieChart()
    LinePlot()
    messagebox.showinfo("Image Extraction", "3 Images of the Charts were saved!")

def add_subjects():
    global Data_df, current_web_scraping_source_index

    method = method_opt.get()

    flag = askyesno("Confirm Data Collection",f"Are you sure you're ready to collect data with the method: {method}") #ελέγχω αν σίγουρα θέλει να κάνει web scrape ο χρήστης

    if not flag:
        return

    source_name = ""

    if method == "Harvard":
        source = sources_web_scraping[0]
        source_name = source["name"]
        print(f"[{source_name}] Status: Starting Web Scraping Data Collection...")
        try:
            result_df = Scraper(source['url'], source['name'])
        except:
            print(f"[{source_name}] Status: Failed")
            return
        current_web_scraping_source_index +=1
    elif method == "Class Central":
        source = sources_web_scraping[1]
        source_name = source["name"]
        print(f"[{source_name}] Status: Starting Web Scraping Data Collection...")
        try:
            result_df = Scraper(source['url'], source['name'])
        except:
            print(f"[{source_name}] Status: Failed")
            return
        current_web_scraping_source_index += 1
    elif method == "Coursera":
        source = sources_web_scraping[2]
        source_name = source["name"]
        print(f"[{source_name}] Status: Starting Web Scraping Data Collection...")
        try:
            result_df = Scraper(source['url'], source['name'])
        except:
            print(f"[{source_name}] Status: Failed")
            return
        current_web_scraping_source_index += 1
    elif method == "Udemy Free":
        source_name = "Udemy (API)"
        print(f"[{source_name}] Status: Starting API Data Collection...")
        result_df = freeUdemyCourse()

    if result_df is not None and not result_df.empty:
        frames = [Data_df, result_df]
        Data_df = pd.concat(frames)

        Data_df = normalize_data(Data_df)

        print(f"[{source_name}] Status: Success")
        messagebox.showinfo("Success", f"Συλλέχθηκαν {len(result_df)} μαθήματα από {source_name}")

        listbox.delete(0, tk.END)
        listbox.pack()

        for title in Data_df["Title"]:
            listbox.insert(END, title)
    else:
        print(f"[{source_name}] Status: Failed")
        messagebox.showerror("Error", "Αποτυχία συλλογής δεδομένων.")



def export_data():
    global Data_df
    if Data_df.empty:
        messagebox.showwarning("Warning", "Δεν υπάρχουν δεδομένα για εξαγωγή.")
        return


    flag = askyesno("Confirm Data Exportation", "Are you sure you're ready?")
    if not flag:
        return


    filename = "courses_1115515.csv"
    AppendOrNot=askyesno("Confirm Append Mode", "Append Mode or Rewrite Mode to CSV(Yes for append, No for Rewrite)")
    mode="a" if AppendOrNot else "w"
    header=False if AppendOrNot else True

    Data_df = Data_df.drop_duplicates(subset=["Title"])


    if AppendOrNot and mode=="a":
        new_data=delete_duplicates_in_csv()
        if new_data.empty:
            messagebox.showinfo("CSV Export Info", "No new Data were found!")
            return
        new_data.to_csv(filename,mode=mode, index=False, header=header)
    else:
        Data_df.to_csv(filename, mode=mode,index=False, header=header)
    print(f"[System] Status: Export to {filename} Successful")
    messagebox.showinfo("Export Success", f"Τα δεδομένα αποθηκεύτηκαν στο {filename}")



def delete_duplicates_in_csv():
    global Data_df
    filename = "courses_1115515.csv"

    try:
        pdd = pd.read_csv(filename)

        palioi = set(pdd["Title"])
        neoi = set(Data_df["Title"])
        pragmatika_neoi_titloi = neoi - palioi

        new_data_only = Data_df[Data_df["Title"].isin(pragmatika_neoi_titloi)]

        return new_data_only

    except FileNotFoundError:
        return Data_df

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1280x720")
    root.title("Web scraper Python ΑΓΓΕΛΟΠΟΥΛΟΣ ΓΡΗΓΟΡΙΟΣ ΠΑΝΑΓΙΩΤΗΣ 1115514 ΚΟΠΙΤΣΑΣ ΝΙΚΟΛΑΣ 115515")

    frame1 = tk.Frame(root, width=500, height=500)
    paddingYVal = 10
    # ebala frame gia na ta exw ola
    frame1.pack(pady=20)
    addSubjectsBtn = tk.Button(frame1, text="Προσθήκη μαθημάτων", width=35, command=add_subjects)
    addSubjectsBtn.pack(pady=paddingYVal, side="top")

    methods = ["Harvard","Class Central","Coursera", "Udemy Free"]
    method_opt = StringVar(value="Harvard")  # Default τιμή το Web Scraping
    methodMenu = OptionMenu(frame1, method_opt, *methods)
    methodMenu.config(width=15)
    methodMenu.pack(pady=5)

    addSubjectsBtn = tk.Button(frame1, text="Εμφάνιση metadata μαθημάτων", width=35, command=readMetadata)
    addSubjectsBtn.pack(pady=paddingYVal)
    # Dropdown options
    days = [""]
    # Selected option variable
    opt = StringVar(value="")
    dropdownMenu = OptionMenu(frame1, opt, *days)
    addSubjectsBtn = tk.Button(frame1, text="Επιλογή κριτηρίων", width=25, command=lambda: filtersWindow(days, dropdownMenu))
    addSubjectsBtn.pack(pady=paddingYVal)

    # Dropdown menu
    dropdownMenu.pack(pady=5)

    showGraphsBtn = tk.Button(frame1, text=" Εμφάνιση γραφημάτων", width=35, command=show_graphs)
    showGraphsBtn.pack(pady=paddingYVal)

    exportsBtn = tk.Button(frame1, text="Εξαγωγή δεδομένων σε CSV", width=35, command=export_data)
    exportsBtn.pack(pady=paddingYVal)

    listbox = tk.Listbox(frame1, width=100, font=("Calibri", 11))
    listbox.pack(pady=20, padx=10)

    root.mainloop()