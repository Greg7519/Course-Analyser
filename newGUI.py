import pandas as pd
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from tkinter.messagebox import askyesno

# Δικά σας imports
from readFunctions import readMetadata,readFromCSVWithFilters
from apiCalls import *
from plots import *
from scraper import *

# Ρύθμιση εμφάνισης
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Global Μεταβλητές (από το παλιό UI)
Data_df = pd.DataFrame()
current_web_scraping_source_index = 0

sources_web_scraping = [
    {"name": "Harvard", "url": "https://pll.harvard.edu/catalog"},
    {"name": "Class Central", "url": "https://www.classcentral.com/collection/top-free-online-courses"},
    {"name": "Coursera", "url": "https://www.coursera.org/search?query=web%20development&language=English&productDifficultyLevel=Beginner&productDifficultyLevel=Intermediate&productDifficultyLevel=Advanced&productTypeDescription=Courses&topic=Computer%20Science&sortBy=BEST_MATCH"}
]

# --- ΚΛΑΣΗ ΓΙΑ ΤΟ ΝΕΟ ΠΑΡΑΘΥΡΟ ΦΙΛΤΡΩΝ ---
class CriteriaWindow(ctk.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.geometry("400x500")
        self.title("Επιλογή Κριτηρίων")
        self.attributes('-topmost', True)

        self.label = ctk.CTkLabel(self, text="Εισαγωγή Παραμέτρων", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.pack(pady=(30, 20))
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.inpLabels= ["Θεματική κατηγορία", "Δυσκολία", "Γλώσσα", "Μέγιστο κόστος"]
        self.inputs = []
        for i in range(4):
            entry = ctk.CTkEntry(self, placeholder_text=f"{self.inpLabels[i]}...", width=280, height=40)
            entry.pack(pady=10)
            self.inputs.append(entry)

        self.submit_btn = ctk.CTkButton(self, text="✅ Αποθήκευση & Κλείσιμο",
                                        command=self.save_and_close,
                                        fg_color="#10b981", hover_color="#059669")
        self.submit_btn.pack(pady=30)

    def on_close(self):
        self.parent.popup = None
        self.destroy()

    def save_and_close(self):
        results = [entry.get() for entry in self.inputs]
        print(f"Αποθηκευμένα Κριτήρια: {results}")
        # Σημείωση: Αν θέλετε, μπορείτε εδώ να καλέσετε την παλιά σας filtersWindow()
        readFromCSVWithFilters(results[3], results[2],results[0], results[1])
        self.parent.update_display("Φίλτρα Εφαρμόστηκαν", f"Τα κριτήρια που επιλέχθηκαν:\n{results}")
        self.parent.popup = None
        self.destroy()


class ModernDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("🎓 Course Analytics Dashboard - Web Scraper")
        self.geometry("1100x650")
        self.minsize(800, 500)

        # ------------------ LAYOUT CONFIGURATION ------------------
        self.grid_columnconfigure(0, weight=1)  # Sidebar column
        self.grid_columnconfigure(1, weight=4)  # Main content column
        self.grid_rowconfigure(0, weight=1)

        # ==================== SIDEBAR FRAME ====================
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar_frame.grid_rowconfigure(7, weight=1)

        self.popup = None

        # App Title
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Course Analytics",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 20), sticky="w")

        # Section: Actions
        self.action_label = ctk.CTkLabel(self.sidebar_frame, text="MAIN ACTIONS",
                                         font=ctk.CTkFont(size=11, weight="bold"), text_color="gray")
        self.action_label.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="w")

        # Dropdown Πηγών (Αντικαθιστά το methodMenu)
        self.course_dropdown = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=["Harvard", "Class Central", "Coursera", "Udemy Free"]
        )
        self.course_dropdown.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        # Προσθήκη Μαθημάτων
        self.btn_add_course = ctk.CTkButton(self.sidebar_frame, text="➕ Προσθήκη Μαθημάτων", anchor="w",
                                            command=self.add_subjects)
        self.btn_add_course.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        # Metadata
        self.btn_view_metadata = ctk.CTkButton(self.sidebar_frame, text="📋 Εμφάνιση Metadata", anchor="w",
                                               command=self.view_metadata_action)
        self.btn_view_metadata.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

        # Section: Filters & Analytics
        self.filter_label = ctk.CTkLabel(self.sidebar_frame, text="FILTERS & ANALYSIS",
                                         font=ctk.CTkFont(size=11, weight="bold"), text_color="gray")
        self.filter_label.grid(row=5, column=0, padx=20, pady=(20, 5), sticky="w")

        self.btn_open_criteria = ctk.CTkButton(self.sidebar_frame, text="🔍 Επιλογή Κριτηρίων", anchor="w",
                                               command=self.open_criteria_popup)
        self.btn_open_criteria.grid(row=6, column=0, padx=20, pady=5, sticky="ew")

        self.btn_show_charts = ctk.CTkButton(self.sidebar_frame, text="📈 Εμφάνιση Γραφημάτων", anchor="w",
                                             command=self.show_charts_action)
        self.btn_show_charts.grid(row=7, column=0, padx=20, pady=5, sticky="new")

        # Section: Export
        self.btn_export_csv = ctk.CTkButton(self.sidebar_frame, text="📥 Εξαγωγή σε CSV", fg_color="transparent",
                                            border_width=1, command=self.export_csv_action)
        self.btn_export_csv.grid(row=8, column=0, padx=20, pady=20, sticky="ew")

        # ==================== MAIN CONTENT FRAME ====================
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)

        # Header within content area
        self.content_title = ctk.CTkLabel(self.content_frame, text="Καλώς ορίσατε στο Course Analytics",
                                          font=ctk.CTkFont(size=24, weight="bold"))
        self.content_title.grid(row=0, column=0, padx=10, pady=(10, 20), sticky="w")

        # Dynamic display box (Αντικαθιστά το παλιό tk.Listbox)
        self.display_box = ctk.CTkTextbox(self.content_frame, activate_scrollbars=True, font=ctk.CTkFont(size=14))
        self.display_box.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)


    # ------------------ HELPER LOGIC ------------------
    def update_display(self, title, message):
        """Ενημερώνει τον κεντρικό τίτλο και το Textbox"""
        self.content_title.configure(text=title)
        self.display_box.delete("0.0", "end")
        self.display_box.insert("0.0", message)

    def open_criteria_popup(self):
        if self.popup is None or not self.popup.winfo_exists():
            self.popup = CriteriaWindow(self)
        else:
            self.popup.focus()

    # ------------------ CORE ACTIONS ------------------
    def add_subjects(self):
        global Data_df, current_web_scraping_source_index

        method = self.course_dropdown.get()

        flag = askyesno("Confirm Data Collection", f"Are you sure you're ready to collect data with the method: {method}")

        if not flag:
            return

        source_name = ""
        result_df = None

        if method == "Harvard":
            source = sources_web_scraping[0]
            source_name = source["name"]
            print(f"[{source_name}] Status: Starting Web Scraping...")
            try:
                result_df = Scraper(source['url'], source['name'])
            except Exception as e:
                print(f"[{source_name}] Status: Failed - {e}")
                messagebox.showerror("Error", f"Αποτυχία συλλογής από {source_name}.")
                return
            current_web_scraping_source_index += 1

        elif method == "Class Central":
            source = sources_web_scraping[1]
            source_name = source["name"]
            print(f"[{source_name}] Status: Starting Web Scraping...")
            try:
                result_df = Scraper(source['url'], source['name'])
            except Exception as e:
                print(f"[{source_name}] Status: Failed - {e}")
                messagebox.showerror("Error", f"Αποτυχία συλλογής από {source_name}.")
                return
            current_web_scraping_source_index += 1

        elif method == "Coursera":
            source = sources_web_scraping[2]
            source_name = source["name"]
            print(f"[{source_name}] Status: Starting Web Scraping...")
            try:
                result_df = Scraper(source['url'], source['name'])
            except Exception as e:
                print(f"[{source_name}] Status: Failed - {e}")
                messagebox.showerror("Error", f"Αποτυχία συλλογής από {source_name}.")
                return
            current_web_scraping_source_index += 1

        elif method == "Udemy Free":
            source_name = "Udemy (API)"
            print(f"[{source_name}] Status: Starting API Data Collection...")
            try:
                result_df = freeUdemyCourse()
            except Exception as e:
                print(f"[{source_name}] Status: Failed - {e}")
                messagebox.showerror("Error", "Αποτυχία κλήσης API Udemy.")
                return

        # Επεξεργασία και προβολή των δεδομένων
        if result_df is not None and not result_df.empty:
            frames = [Data_df, result_df]
            Data_df = pd.concat(frames)
            # Υποθέτουμε ότι η normalize_data είναι defined στο scraper.py ή αλλού
            Data_df = normalize_data(Data_df)

            print(f"[{source_name}] Status: Success")
            messagebox.showinfo("Success", f"Συλλέχθηκαν {len(result_df)} μαθήματα από {source_name}")

            # Ανανέωση του Display Box αντί για το παλιό Listbox
            titles_text = "\n".join(Data_df["Title"].dropna().tolist())
            self.update_display(f"Αποτελέσματα: {source_name}", f"Συνολικά Μαθήματα Στη Μνήμη: {len(Data_df)}\n\nΛίστα Μαθημάτων:\n{'-'*50}\n{titles_text}")
        else:
            print(f"[{source_name}] Status: Failed / No Data")
            messagebox.showwarning("Warning", "Δεν βρέθηκαν δεδομένα ή υπήρξε αποτυχία.")

    def view_metadata_action(self):
        # Καλεί τη δική σας συνάρτηση από το readFunctions.py
        try:
            readMetadata()
            self.update_display("Εμφάνιση Metadata", "Η λειτουργία Metadata εκτελέστηκε σε εξωτερικό παράθυρο/κονσόλα.")
        except Exception as e:
            messagebox.showerror("Error", f"Αποτυχία εμφάνισης Metadata: {e}")

    def show_charts_action(self):
        # Καλεί τα plots από το plots.py
        try:
            barPlot()
            PieChart()
            LineChart()
            messagebox.showinfo("Image Extraction", "3 Images of the Charts were saved!")
            self.update_display("Εμφάνιση Γραφημάτων", "Τα γραφήματα δημιουργήθηκαν με επιτυχία και οι εικόνες αποθηκεύτηκαν!")
        except Exception as e:
            messagebox.showerror("Error", f"Αποτυχία δημιουργίας γραφημάτων: {e}")

    # ------------------ CSV EXPORT LOGIC ------------------
    def export_csv_action(self):
        global Data_df
        if Data_df.empty:
            messagebox.showwarning("Warning", "Δεν υπάρχουν δεδομένα για εξαγωγή.")
            return

        flag = askyesno("Confirm Data Exportation", "Are you sure you're ready?")
        if not flag:
            return

        filename = "courses_1115515.csv"
        AppendOrNot = askyesno("Confirm Append Mode", "Append Mode or Rewrite Mode to CSV? (Yes for append, No for Rewrite)")
        mode = "a" if AppendOrNot else "w"
        header = False if AppendOrNot else True

        # Αφαίρεση διπλότυπων από το τρέχον dataframe πριν την εξαγωγή
        Data_df = Data_df.drop_duplicates(subset=["Title"])

        if AppendOrNot and mode == "a":
            new_data = self.delete_duplicates_in_csv()
            if new_data.empty:
                messagebox.showinfo("CSV Export Info", "No new Data were found!")
                return
            new_data.to_csv(filename, mode=mode, index=False, header=header)
        else:
            Data_df.to_csv(filename, mode=mode, index=False, header=header)

        print(f"[System] Status: Export to {filename} Successful")
        self.update_display("Εξαγωγή Δεδομένων", f"✅ Τα δεδομένα αποθηκεύτηκαν επιτυχώς στο αρχείο '{filename}'.")
        messagebox.showinfo("Export Success", f"Τα δεδομένα αποθηκεύτηκαν στο {filename}")

    def delete_duplicates_in_csv(self):
        """Ελέγχει αν υπάρχουν ήδη τα μαθήματα στο CSV για να μην εγγραφούν ξανά σε Append Mode"""
        global Data_df
        filename = "courses_1115515.csv"
        try:
            pdd = pd.read_csv(filename)
            palioi = set(pdd["Title"].dropna())
            neoi = set(Data_df["Title"].dropna())
            pragmatika_neoi_titloi = neoi - palioi

            new_data_only = Data_df[Data_df["Title"].isin(pragmatika_neoi_titloi)]
            return new_data_only
        except FileNotFoundError:
            return Data_df


if __name__ == "__main__":
    app = ModernDashboard()
    app.mainloop()