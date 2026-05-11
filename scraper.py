import requests
import urllib.parse
from bs4 import BeautifulSoup
def HarvardScraper(append, url):
    harvardCourses:{}
    params = {'max_price':1500,'keywords':'coding','duration_in_weeks[3]':3}
    if append==False:
        # Fetch and parse the page
        url = url +"?" + urllib.parse.urlencode(params)
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
        # Find the main content container
        content = soup.find('div', class_='main-wrapper grid-container full')
        if content:
            for div in content.find_all("div", class_='views-row'):
                # parser price, checking each div once
                for priceDetails in div.find_all("div",class_='field field---extra-field-pll-extra-field-price field--name-extra-field-pll-extra-field-price field--type- field--label-visually_hidden'):
                    print(priceDetails.text)
                for courseHeader in div.find_all("div",class_='field field--name-title field--type-string field--label-hidden field__items'):
                    print(courseHeader.text)
                for courseDetails in div.find_all("div",class_='text-teaser field field--name-field-summary field--type-text field--label-hidden field__items'):
                    print(courseDetails.text)
                for duration in div.find_all("div",class_="field field---extra-field-pll-extra-field-duration field--name-extra-field-pll-extra-field-duration field--type- field--label-visually_hidden"):
                    print(duration.text)

        else:
            print("No article content found.")

HarvardScraper(False,url="https://pll.harvard.edu/catalog")