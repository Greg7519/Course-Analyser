# This is a sample Python script.
import tkinter as tk
from readFunctions import readMetadata
from getUserInput import filtersWindow
from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import askyesno

from numpy.ma.core import append, size

from scraper import *


scraped_data_df = pd.DataFrame()
current_web_scraping_source_index = 0

sources_api = [
    {"name": "Harvard", "url": "https://pll.harvard.edu/catalog"},
    {"name": "Udemy", "url": "https://www.udemy.com/courses/free/"},
    {"name": "Coursera", "url": "https://www.coursera.org/courses?query=free"}
]

sources_web_scraping=[
    {"name": "Harvard", "url": "https://pll.harvard.edu/catalog"},
    {"name": "Class Central", "url": "https://www.classcentral.com/collection/top-free-online-courses"},
    #στο Coursera εχουμε βαλει να εχουμε συγκεκριμενα αποτελεσματα για πιο ευκολο webscaping αφαιρωντας επιλογες οπως difficulty=mixed, language != English etc
    {"name": "Coursera", "url": "https://www.coursera.org/search?query=web%20development&language=English&productDifficultyLevel=Beginner&productDifficultyLevel=Intermediate&productDifficultyLevel=Advanced&productTypeDescription=Courses&topic=Computer%20Science&sortBy=BEST_MATCH"}
]


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

    AppendOrNot=askyesno("Confirm Append Mode", "Append Mode or Rewrite Mode to CSV(Yes for append, No for Rewrite)")
    mode="a" if AppendOrNot else "w"
    header=False if AppendOrNot else True
    if scraped_data_df.empty:
        messagebox.showwarning("Warning", "Δεν υπάρχουν δεδομένα για εξαγωγή.")
        return

    if flag:
        filename = "courses_1115515.csv"
        if AppendOrNot and mode=="a":
            delete_duplicates_in_csv().to_csv(filename,mode=mode, index=False, header=header)
        else:
            scraped_data_df.to_csv(filename, mode=mode,index=False, header=header)
        print(f"[System] Status: Export to {filename} Successful")
        messagebox.showinfo("Export Success", f"Τα δεδομένα αποθηκεύτηκαν στο {filename}")



def delete_duplicates_in_csv():
    global scraped_data_df
    filename = "courses_1115515.csv"

    try:
        pdd = pd.read_csv(filename)

        palioi = set(pdd["Title"])
        neoi = set(scraped_data_df["Title"])
        pragmatika_neoi_titloi = neoi - palioi

        new_data_only = scraped_data_df[scraped_data_df["Title"].isin(pragmatika_neoi_titloi)]

        return new_data_only

    except FileNotFoundError:
        return scraped_data_df

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1280x720")
    root.title("Web scraper Python")

    frame1 = tk.Frame(root, width=500, height=500)
    paddingYVal = 10
    # ebala frame gia na ta exw ola
    frame1.pack(pady=20)
    addSubjectsBtn = tk.Button(frame1, text="Προσθήκη μαθημάτων", width=35, command=add_subjects)
    addSubjectsBtn.pack(pady=paddingYVal, side="top")

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

    showGraphsBtn = tk.Button(frame1, text=" Εμφάνιση γραφημάτων", width=35)
    showGraphsBtn.pack(pady=paddingYVal)

    exportsBtn = tk.Button(frame1, text="Εξαγωγή δεδομένων σε CSV", width=35, command=export_data)
    exportsBtn.pack(pady=paddingYVal)

    listbox = tk.Listbox(frame1, width=100, font=("Calibri", 11))
    listbox.pack(pady=20, padx=10)

    root.mainloop()