import requests
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path
import json
import numpy as np

load_dotenv()
dotenv_path = Path("apiKeys.env")
load_dotenv(dotenv_path=dotenv_path)

def exportDataFromApi(arrayOfDict):
    df = pd.DataFrame(arrayOfDict)
    df.to_csv('courses_1115515.csv', index=False)


def freeUdemyCourse():
    URL = "https://paid-udemy-course-for-free.p.rapidapi.com/?page=0"

    try:
        # Send a simple GET request
        headers = {
            'Content-Type': 'application/json',
            'x-rapidapi-host': os.getenv("UDEMY_HOST"),
            'x-rapidapi-key': os.getenv("UDEMY_KEY")
        }
        response = requests.get(URL, headers=headers)
        response.raise_for_status()  # Trigger error catch on bad status codes

        # Parse json data
        catalog_data = response.json()
        print(json.dumps(catalog_data, indent=4, ensure_ascii=False))
        courseData = []

        # Example: Print beginner course paths
        for course in catalog_data:
            courseVals = {}
            courseVals['Title'] = course.get('title')
            courseVals['Price (in $)'] = np.ceil(float(course.get('org_price').replace("$", "")))
            courseVals['Difficulty'] = 'unknown'
            courseVals['Subject Category'] = course.get('category')
            courseVals['Provider'] = "Udemy"
            courseVals['Course Language'] = course.get('language')
            courseVals['Course Length (in Days)'] = round(course.get('duration')/24,2)
            courseData.append(courseVals)

        df = pd.DataFrame(courseData)
        return df

    except requests.exceptions.RequestException as error:
        print(f"API Fetch Failure: {error}")
