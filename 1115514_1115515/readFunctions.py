import tkinter.messagebox
import numpy as np
import pandas as pd
import customtkinter as ctk
from compositeScore import  calcCompositeScore
from tkinter import *
from numpy.f2py.auxfuncs import l_and
from scrollableFrame import ScrollableFrame


def readTop3Subjects():
    """
    Διαβάζει το filtered.csv και εμφανίζει τα κορυφαία (έως 3) μαθήματα
    σε έναν μοντέρνο πίνακα CustomTkinter.
    """
    try:
        df = pd.read_csv("filtered.csv", delimiter=',')
    except FileNotFoundError:
        tkinter.messagebox.showerror("Error", "Το αρχείο 'filtered.csv' δεν βρέθηκε. Εφαρμόστε πρώτα φίλτρα!")
        return

    rows, cols = df.shape
    if rows < 1:
        tkinter.messagebox.showerror("Error", "Το αρχείο δεν έχει περιεχόμενο (Improper file).")
        return

    # Υπολογισμός των γραμμών που θα εμφανιστούν
    topRows = min(rows, 3)

    # Δημιουργία Μοντέρνου Popup Παραθύρου
    window = ctk.CTkToplevel()  # Βγάλτε το 'self' αν δεν είναι μέθοδος κλάσης
    window.title("🏆 Top Subjects")
    window.geometry("1100x400")
    window.attributes('-topmost', True)

    # Τίτλος Πίνακα
    lbl_title = ctk.CTkLabel(window, text=f"Top {topRows} Recommended Subjects",
                             font=ctk.CTkFont(size=22, weight="bold"))
    lbl_title.pack(pady=(15, 5))

    # Scrollable Frame που θα λειτουργήσει ως Πίνακας
    table_frame = ctk.CTkScrollableFrame(window, corner_radius=10)
    table_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # --- Κατασκευή Κεφαλίδων (Headers) ---
    column_names = df.columns
    for j, col in enumerate(column_names):
        header_lbl = ctk.CTkLabel(
            table_frame,
            text=str(col),
            font=ctk.CTkFont(weight="bold", size=13),
            fg_color="#1f538d",  # Μοντέρνο μπλε χρώμα για το header
            text_color="white",
            corner_radius=6,
            height=35
        )
        header_lbl.grid(row=0, column=j, padx=2, pady=2, sticky="nsew")
        # Επιτρέπει στις στήλες να απλώνονται ομοιόμορφα
        table_frame.grid_columnconfigure(j, weight=1)

    # --- Κατασκευή Κελιών Δεδομένων (Data Rows) ---
    for i in range(topRows):
        for j in range(cols):
            val = str(df.values[i][j])

            # Χρησιμοποιούμε Textbox αντί για Label ώστε τα μεγάλα κείμενα να κάνουν wrap
            cell_box = ctk.CTkTextbox(
                table_frame,
                height=60,
                wrap="word",
                fg_color="#2b2b2b",  # Σκούρο γκρι για τα κελιά
                corner_radius=6
            )
            cell_box.insert("0.0", val)
            cell_box.configure(state="disabled")  # Κλείδωμα για να είναι Read-Only

            cell_box.grid(row=i + 1, column=j, padx=2, pady=2, sticky="nsew")
def readMetadata():
    """
    Διαβάζει το courses_1115515.csv και εμφανίζει τα metadata
    σε έναν μοντέρνο πίνακα CustomTkinter.
    """
    try:
        try:
            df = pd.read_csv("courses_1115515.csv", delimiter=',')
        except FileNotFoundError:
            tkinter.messagebox.showerror("Error", "Το αρχείο 'courses_1115515.csv' δεν βρέθηκε. Κάντε πρώτα εξαγωγή!")
            return

        rows, cols = df.shape
        if rows < 1:
            tkinter.messagebox.showerror("Error", "Το αρχείο δεν έχει περιεχόμενο (Improper file).")
            return

        # Δημιουργία Μοντέρνου Popup Παραθύρου
        window = ctk.CTkToplevel()  # Βγάλτε το 'self' αν η συνάρτηση είναι εκτός κλάσης
        window.title("📋 Courses Metadata")
        window.geometry("1200x700")
        window.attributes('-topmost', True)

        # Τίτλος Πίνακα
        lbl_title = ctk.CTkLabel(window, text=f"Προβολή Metadata (Συνολικά Μαθήματα: {rows})",
                                 font=ctk.CTkFont(size=22, weight="bold"))
        lbl_title.pack(pady=(15, 5))

        # Scrollable Frame που θα λειτουργήσει ως Πίνακας
        table_frame = ctk.CTkScrollableFrame(window, corner_radius=10)
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # --- Κατασκευή Κεφαλίδων (Headers) ---
        column_names = df.columns
        for j, col in enumerate(column_names):
            header_lbl = ctk.CTkLabel(
                table_frame,
                text=str(col),
                font=ctk.CTkFont(weight="bold", size=13),
                fg_color="#1f538d",  # Μοντέρνο μπλε χρώμα για το header
                text_color="white",
                corner_radius=6,
                height=35
            )
            header_lbl.grid(row=0, column=j, padx=2, pady=2, sticky="nsew")
            # Επιτρέπει στις στήλες να απλώνονται ομοιόμορφα
            table_frame.grid_columnconfigure(j, weight=1)

        # --- Κατασκευή Κελιών Δεδομένων (Data Rows) ---
        # Αν τα δεδομένα είναι πάρα πολλά (π.χ. > 500 γραμμές), προσθέτουμε ένα όριο
        # για να μην "παγώσει" το UI από τη δημιουργία χιλιάδων widgets.
        display_rows = min(rows, 300)  # Προβάλλει μέχρι 300 γραμμές για ασφάλεια (αλλάξτε το αν θέλετε)

        if rows > 300:
            lbl_title.configure(text=f"Προβολή Metadata (Εμφάνιση πρώτων 300 από {rows} μαθήματα)")

        for i in range(display_rows):
            for j in range(cols):
                val = str(df.values[i][j])

                # Χρησιμοποιούμε Textbox αντί για Label ώστε τα μεγάλα κείμενα να κάνουν wrap
                cell_box = ctk.CTkTextbox(
                    table_frame,
                    height=60,
                    wrap="word",
                    fg_color="#2b2b2b",  # Σκούρο γκρι για τα κελιά
                    corner_radius=6
                )
                cell_box.insert("0.0", val)
                cell_box.configure(state="disabled")  # Κλείδωμα για να είναι Read-Only

                cell_box.grid(row=i + 1, column=j, padx=2, pady=2, sticky="nsew")

    except Exception as E:
        tkinter.messagebox.showerror("Error", f"Σφάλμα κατά την προβολή: {E}")
        print("Error occurred:", E)


def readFromCSVWithFilters(maxCost,language,category,difficulty):
    try:
        df = pd.read_csv("courses_1115515.csv", delimiter=',')
        resDf = pd.DataFrame(columns=["Title", "Price (in $)", "Difficulty","Subject Category","Provider","Course Length (in Days)","Course Language"])
        rows, cols = df.shape
        if(rows<1):
            tkinter.messagebox.showerror("Error", "File not having contents/Improper file")
            return
        else:
            tkinter.messagebox.showinfo("Filters applied", "File saved successfully!")

        # adding all the other rows into the grid
        column_names = df.columns
        i = 0

        for i in range(rows):
            for j in range(cols):

                diffComp = (df.values[i][2].lower() == difficulty.lower() or difficulty == '')
                categoryComp = (df.values[i][3].lower() == category.lower() or category == '')
                maxCostComp = (maxCost == '' or df.values[i][1] <= float(maxCost))
                langComp = (df.values[i][5].lower() == language.lower() or language == '')
                if (diffComp and categoryComp and maxCostComp and langComp):

                    if(j==0):
                        # need to update menu

                        resDf.loc[resDf.shape[0]]= df.loc[i]

        if(resDf.shape[0]<1):
            tkinter.messagebox.showerror("Error", "No data found with these criteria!")
            return
        else:
            resDf.to_csv("filtered.csv", index=False)
            calcCompositeScore()

    except:
        tkinter.messagebox.showerror("Error", "File not having contents/Improper file")
        print('Error occured!')


