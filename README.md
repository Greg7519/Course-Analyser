# 🎓 Course Analyser

> **Finding the perfect course for you!**  
Course Analyser helps learners discover optimal online courses by scraping top platforms, filtering results, and computing an **intelligent recommendation score** based on cost and duration.

---

## ✨ Features

- 🏆 **Top 5 Longest Courses:** Easily view the top 5 courses with the longest duration (in days).
- 📊 **Matplotlib Visualizations:** Dynamic price vs. duration (in days) scatter plots and diagrams to visualize market trends.
- 🎯 **Difficulty Filtering:** Narrow down your search by filtering courses according to difficulty level (Beginner, Intermediate, Advanced).
- 🧠 **Smart Recommendation Algorithm:** Ranks courses using a weighted composite score that optimizes cost and time efficiency.
- 🎨 **Modern Desktop GUI:** Built with a custom, clean `customtkinter` layout for an intuitive user experience.
- 🐼 **Fast Data Processing:** Uses `pandas` under the hood for efficient data cleaning, manipulation, and filtering.

---

## 💡 Smart Recommendation Algorithm (Αλγόριθμος Έξυπνων Συστάσεων)

The course rank is determined by a weighted **Composite Score** where an **ideal score equal to $1.0$** represents the maximum recommendation value.

### 📐 Mathematical Formulation

1. **Normalized Cost Factor:**
   $$ \text{Cost Factor} = \left(1 - \frac{\text{Price}}{\text{Price}_{\max}}\right) \times 0.5 $$
   *(Lower cost results in a higher score factor)*

2. **Normalized Duration Factor:**
   $$ \text{Duration Factor} = \begin{cases} \left(1 - \frac{\text{Duration}}{\text{Duration}_{\max}}\right) \times 0.5 & \text{if } \text{Duration} > 0 \\ 0 & \text{if } \text{Duration} = 0 \end{cases} $$
   *(Lower duration yields a higher score factor; missing/zero duration yields 0)*

3. **Composite Score:**
   $$ \text{Score} = 0.6 \times \text{Cost Factor} + 0.4 \times \text{Duration Factor} $$

### ⚙️ Scoring Nuances & Edge Cases

- **Why Weight Cost Higher (0.6 vs 0.4)?** Cost data is reliably retrieved across all source platforms, whereas course duration is occasionally missing ($0$). Assigning a higher weight to cost ensures fairer overall rankings.
- **Handling Uniform Datasets:** If min and max values are equal (i.e., all courses share the exact same price or duration), a baseline weight of **0.5** is assigned to maintain mathematical balance and avoid division by zero.

---

## 🌐 Data Sources & Web Scraping

Course Analyser gathers data dynamically using custom web scrapers and direct API integrations:

| Source | Extraction Method |
| :--- | :--- |
| 📚 **Coursera** | Web Scraper |
| 🏛️ **Harvard Online** | Web Scraper |
| 🌐 **Class Central** | Web Scraper |
| 🎓 **Free Udemy Courses** | Official API |

---

## 🛠️ Tech Stack

- **GUI:** `customtkinter`
- **Data Manipulation:** `pandas`
- **Visualization:** `matplotlib`
- **Scraping & API:** `requests`, `BeautifulSoup`

---

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/course-analyser.git](https://github.com/your-username/course-analyser.git)
   cd course-analyser
