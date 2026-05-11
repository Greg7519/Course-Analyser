import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import random
import json


def HarvardScraper(url):
    all_Harvard_courses = []
    number_of_courses = 10


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

        course_length = index.get("data-course-length") or "N/A"

        if course_length != "N/A":
            if course_length.lower().find("week") != -1:
                course_length = course_length[:course_length.lower().find("week")]
                course_length = str(7 * int(course_length))
            if course_length.lower().find("month") != -1:
                course_length = course_length[:course_length.lower().find("month")]
                course_length = str(31 * int(course_length))

        course_language = index.get("data-course-language") or "Unknown"

        all_Harvard_courses.append({
                "Title": title,
                "Price (in $)": price,
                "Difficulty": difficulty,
                "Subject Category": subject_category,
                "Provider": provider,
                "Course Length (in Days)": course_length,
                "Course Language": course_language
            })

    df = pd.DataFrame(all_Harvard_courses)

    return df


def ClassCentralScraper(url):
    all_ClassCentral_courses = []
    number_of_courses = 10



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
                            hours = (float(parts[0]) + float(parts[1])) / 2
                        else:
                            hours = float(temp[i - 1])


        # final conversion
        course_length = weeks * hours if weeks else hours



        all_ClassCentral_courses.append({
                "Title": title,
                "Price (in $)": price,
                "Difficulty": difficulty,
                "Subject Category": subject_category,
                "Provider": provider,
                "Course Length (in Days)": course_length,
                "Course Language": course_language
            })

    df = pd.DataFrame(all_ClassCentral_courses)

    return df


def Scraper(url, name):
    courses=None
    match name:
        case "Class Central": courses=ClassCentralScraper(url)
        case "Harvard": courses=HarvardScraper(url)

    return courses


def normalize_data(df):
    mapping = {
        'unknown': 'Εύκολο',
        'beginner': 'Εύκολο',
        'introductory': 'Εύκολο',
        'intermediate': 'Μέτριο',
        'advanced': 'Δύσκολο',
        'introductory, intermediate': 'Μέτριο',
        'introductory, intermediate, advanced': 'Μέτριο'
    }

    df['Difficulty'] = df['Difficulty'].str.lower().replace(mapping) #
    df['Course Length (in Days)'] = df['Course Length (in Days)'].replace('N/A', 0)
    df['Price (in $)'] = np.ceil(df['Price (in $)'].replace(np.nan, 0)).astype(int)


    return df




