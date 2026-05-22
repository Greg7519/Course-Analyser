import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import random
import json


def HarvardScraper(url):
    all_Harvard_courses = []
    number_of_courses = 6


    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    # Find the main content container
    content = soup.find('div', class_='main-wrapper grid-container full')

    if not content:
        print("No article content found.")
        return pd.DataFrame(all_Harvard_courses)

    blocks = content.find_all("div", class_='views-row')


    random.shuffle(blocks)

    for block in blocks:

        if len(all_Harvard_courses) >= number_of_courses:
            break

        index = block.find("div", class_="datalayer-values")

        if not index:
            continue

        title = index.get("data-item-name") or "Unknown"
        price = float(index.get("data-course-price")) or np.nan
        difficulty = index.get("data-course-difficulty") or "Unknown"
        subject_category = index.get("data-item-category") or "Unknown"
        provider = index.get("data-course-school") or "Unknown"

        course_len = index.get("data-course-length") or "N/A"

        if course_len != "N/A":
            if course_len.lower().find("week") != -1:
                course_len = course_len[:course_len.lower().find("week")]
                course_length = np.ceil(7 * int(course_len)).astype(int)
            if course_len.lower().find("month") != -1:
                course_len = course_len[:course_len.lower().find("month")]
                course_length = np.ceil(31 * int(course_len)).astype(int)
        else:
            course_length=0 #θεωρουμε οτι αν δεν αναφερει χρόνο για το course ότι ειναι 0


        course_language = index.get("data-course-language") or "Unknown"

        all_Harvard_courses.append({
                "Title": title,
                "Price (in $)": price,
                "Difficulty": difficulty,
                "Subject Category": subject_category,
                "Provider": provider,
                "Course Language": course_language,
                "Course Length (in Days)": course_length,
            })

    df = pd.DataFrame(all_Harvard_courses)

    return df


def ClassCentralScraper(url):
    all_ClassCentral_courses = []
    number_of_courses = 6



    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    # Find the main content container
    content = soup.find('div', class_='catalog-grid__results')

    if not content:
        print("No article content found.")
        return pd.DataFrame(all_ClassCentral_courses)

    blocks = content.find_all("li", class_='bg-white border-all border-gray-light padding-xsmall radius-small margin-bottom-small medium-up-padding-horz-large medium-up-padding-vert-medium course-list-course')


    random.shuffle(blocks)

    for block in blocks:

        if len(all_ClassCentral_courses) >= number_of_courses:
            break

        index = block.find("p", class_="text-2 margin-bottom-xsmall")

        if not index:
            continue

        a_tag = index.find("a", {"data-track-props": True})

        if not a_tag:
            continue

        try:
            props = json.loads(a_tag["data-track-props"])
        except:
            continue

        title=props.get("course_name") or "Unknown"
        course_language = props.get("course_language") or "Unknown"
        difficulty = props.get("course_level") or "Unknown"



        if props.get("course_is_free"):
            price=0
        else:
            price=np.nan


        subject_category = props.get("course_subject")

        if props.get("course_is_university"):
            provider = props.get("course_institution")
        else:
            provider = "Unknown"

        index = block.find("span", class_="text-3 margin-left-small line-tight")

        course_length = index.get_text(strip=True)
        temp = course_length.split()

        weeks = 0
        hours = 0


        if "week" in course_length: #ελέγχουμε αν το course ειναι πανω απο 1 εβδομάδα
            weeks = int(temp[0])


        if "hour" in course_length:
            for i, t in enumerate(temp):
                if "hour" in t:
                        if "-" in temp[i - 1]: #ελεγχουμε αν το course ειναι μέσος όρος ωρών
                            parts = temp[i - 1].split("-")
                            hours = np.ceil((float(parts[0]) + float(parts[1])) / 2).astype(int)
                        else:
                            hours = np.ceil(float(temp[i - 1])).astype(int)


        # final conversion
        course_length = weeks * hours if weeks else hours



        all_ClassCentral_courses.append({
                "Title": title,
                "Price (in $)": price,
                "Difficulty": difficulty,
                "Subject Category": subject_category,
                "Provider": provider,
                "Course Language": course_language,
                "Course Length (in Days)": course_length,

            })

    df = pd.DataFrame(all_ClassCentral_courses)

    return df


def CourseraScraper(url):
    Coursera_courses = []
    number_of_courses = 6



    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')


    blocks = soup.find_all("li", class_='cds-9 css-0 cds-11 cds-grid-item cds-56 cds-64 cds-76 cds-89')

    if not blocks:
        print("No article content found.")
        return pd.DataFrame()

    random.shuffle(blocks)

    for block in blocks:

        if len(Coursera_courses) >= number_of_courses:
            break

        provider_tag = block.find("p", class_="cds-ProductCard-partnerNames css-4s48ix")
        provider = provider_tag.get_text(strip=True) if provider_tag else "N/A"

        title_tag = block.find("h3", class_="cds-CommonCard-title")
        title = title_tag.get_text(strip=True) if title_tag else "N/A"


        price=np.nan

        index1=block.find("div", class_="cds-CommonCard-metadata")
        index2=index1.get_text(strip=True)
        index2=index2.split("Â·")
        difficulty=str(index2[0])
        dur1=index2[2]
        dur1=dur1.split(" ")
        num1=float(dur1[1])
        num2=float(dur1[3])
        mesos_oros=np.ceil((num2+num1)/2).astype(int)
        dur2=dur1[4].lower()

        if "week" in dur2:
            course_length=mesos_oros*7
        elif "month" in dur2:
            course_length=mesos_oros*31
        else:
            course_length=np.nan

        sub1=block.find("h3", class_="cds-CommonCard-title css-6ecy9b")
        subject_category=sub1.get_text(strip=True)





        a_tag = block.find("a", {"data-click-value": True})

        if not a_tag:
            continue

        try:
            props = json.loads(a_tag["data-click-value"])
        except:
            continue
        course=str(props.get("filtersApplied"))
        course=course.split("\'")
        course_language=course[3]
        subject_category=course[19]


        Coursera_courses.append({
            "Title": title,
            "Price (in $)": price,
            "Difficulty": difficulty,
            "Subject Category": subject_category,
            "Provider": provider,
            "Course Length (in Days)": course_length,
            "Course Language": course_language
            })

    df = pd.DataFrame(Coursera_courses)

    return df


def Scraper(url, name):
    courses=None
    match name:
        case "Class Central": courses=ClassCentralScraper(url)
        case "Harvard": courses=HarvardScraper(url)
        case "Coursera": courses=CourseraScraper(url)
    return courses


def normalize_data(df):
    mapping1 = {
        'unknown': 'unknown',
        'beginner': 'beginner',
        'introductory': 'beginner',
        'intermediate': 'intermediate',
        'advanced': 'advanced',
        'introductory, intermediate': 'intermediate',
        'introductory, intermediate, advanced': 'intermediate'
    }


    # 2. Κατηγοριοποίηση των Subject Categories
    mapping2 = {
        # --- COMPUTER SCIENCE & TECH ---
        'computer science': 'Computer Science',
        'programming': 'Computer Science',
        'python': 'Computer Science',
        'programming with javascript': 'Computer Science',
        'development': 'Computer Science',
        'it & software': 'Computer Science',

        # --- BUSINESS & ECONOMICS ---
        'business': 'Business & Management',
        'marketing': 'Business & Management',
        'art & design': 'Business & Management',
        'persuasive leadership': 'Business & Management',
        'finance & accounting': 'Business & Management',
        'office productivity': 'Business & Management',
        'design': 'Business & Management',


        # --- HEALTH & SCIENCE ---
        'health & medicine': 'Health & Science',
        'disease & disorders': 'Health & Science',
        'dementia': 'Health & Science',
        'parasitology': 'Health & Science',
        'biology': 'Health & Science',
        'meditation': 'Health & Science',
        'science': 'Health & Science',

        # --- DATA SCIENCE & STEM ---
        'data science': 'Data Science & STEM',
        'ciencia de datos: fundamentos de r': 'Data Science & STEM',
        'quantum mechanics': 'Data Science & STEM',
        'paleontology': 'Data Science & STEM',
        'environmental science': 'Data Science & STEM',
        'arithmetic circuits': 'Data Science & STEM',

        # --- HUMANITIES & SOCIAL SCIENCES ---
        'social sciences': 'Humanities & Social Sciences',
        'humanities': 'Humanities & Social Sciences',
        'teacher professional development': 'Humanities & Social Sciences',
        'poetry': 'Humanities & Social Sciences',
        'dutch': 'Humanities & Social Sciences',
        'mindfulness': 'Humanities & Social Sciences',
        'self improvement': 'Humanities & Social Sciences',
        'personal development': 'Humanities & Social Sciences',
        'teaching & academics': 'Humanities & Social Sciences',
        'photography & video': 'Humanities & Social Sciences',
        'education & teaching': 'Humanities & Social Sciences'
    }


    df['Difficulty'] = df['Difficulty'].str.lower().str.strip().replace(mapping1)
    df['Subject Category'] = df['Subject Category'].str.lower().str.strip()
    df['Subject Category'] = df['Subject Category'].replace(mapping2)
    df['Price (in $)'] = np.ceil(df['Price (in $)'].replace(np.nan, 0)).astype(int)


    return df