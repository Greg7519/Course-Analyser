import requests
from bs4 import BeautifulSoup
import pandas as pd




def HarvardScraper(append, url):
    all_Harvard_courses = []
    if append == False:
        # Fetch and parse the page
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
        # Find the main content container
        content = soup.find('div', class_='main-wrapper grid-container full')
        if content:
            for block in content.find_all("div", class_='views-row'):
                index=block.find("div", class_="datalayer-values")
                title=index.get("data-item-name")
                price=index.get("data-course-price")
                difficulty=index.get("data-course-difficulty")
                subject_category=index.get("data-item-category")
                provider=index.get("data-course-school")

                course_length=index.get("data-course-length")
                if course_length=="": course_length="Ν/Α"
                if course_length.upper().find("WEEK")!=-1:
                    course_length=course_length[:course_length.upper().find("WEEK")]
                    course_length=str(7*int(course_length))
                if course_length.upper().find("MONTH")!=-1:
                    course_length=course_length[:course_length.upper().find("MONTH")]
                    course_length=str(31*int(course_length))

                course_language=index.get("data-course-language")


                course = {
                    "Title": title,
                    "Price":price,
                    "Difficulty":difficulty,
                    "Subject Category":subject_category,
                    "Provider":provider,
                    "Course Length (in Days)":course_length,
                    "Course Language":course_language
                }
                all_Harvard_courses.append(course)
        else:
            print("No article content found.")

        df = pd.DataFrame(all_Harvard_courses)
        return df



