# This is a sample Python script.
import tkinter as tk
from readMetadata import readMetadata
from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import askyesno

from numpy.ma.core import append

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

    if scraped_data_df.empty:
        messagebox.showwarning("Warning", "Δεν υπάρχουν δεδομένα για εξαγωγή.")
        return

    if flag:
        filename = "courses_115515.csv"
        scraped_data_df.to_csv(filename, index=False)
        print(f"[System] Status: Export to {filename} Successful")
        messagebox.showinfo("Export Success", f"Τα δεδομένα αποθηκεύτηκαν στο {filename}")


if __name__ == "__main__":
    root = tk.Tk()

    root.title("Web scraper Python ΑΓΓΕΛΟΠΟΥΛΟΣ ΓΡΗΓΟΡΙΟΣ ΠΑΝΑΓΙΩΤΗΣ 1115514 ΚΟΠΙΤΣΑΣ ΝΙΚΟΛΑΣ 115515")
    root.geometry("1280x720")

    menubar = tk.Menu(root)

    data_menu = tk.Menu(menubar, tearoff=0)
    data_menu.add_command(label="Συλλογή (API & Scraping)", command=add_subjects)
    data_menu.add_command(label="Εμφάνιση Metadata", command=readMetadata)
    data_menu.add_separator()
    data_menu.add_command(label="Εξαγωγή σε CSV", command=export_data)
    data_menu.add_separator()
    data_menu.add_command(label="Έξοδος", command=root.quit)
    menubar.add_cascade(label="Δεδομένα", menu=data_menu)

    analysis_menu = tk.Menu(menubar, tearoff=0)
    analysis_menu.add_command(label="Εμφάνιση Γραφημάτων")
    menubar.add_cascade(label="Ανάλυση", menu=analysis_menu)

    recommender_menu = tk.Menu(menubar, tearoff=0)
    recommender_menu.add_command(label="Λήψη Προτάσεων")
    menubar.add_cascade(label="Έξυπνες Συστάσεις", menu=recommender_menu)

    root.config(menu=menubar)


    listbox = tk.Listbox(root, width=100, font=("Calibri", 11))
    listbox.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

    root.mainloop()