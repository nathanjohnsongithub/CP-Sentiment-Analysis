# Scraping for yelp using BeautifulSoup
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re

counter = 0

string = 'https://www.yelp.com/biz/buffalo-joes-evanston'
original_length = len(string)
extra_string = '?start='

r = requests.get(string)
regex = re.compile('.*comment.*')
reviews = []
still_pages = True
while(still_pages):
    if (counter == 30):
        break
    try:
        soup = BeautifulSoup(r.text, 'html.parser')
        results = soup.find_all('p', {'class':regex})
        new_reviews = [result.text for result in results]
        reviews.extend(new_reviews)
        counter += 10
        string = string[:original_length]
        string = f"{string}{extra_string}{counter}"
        print(string)
        r = requests.get(string)
    except:
        print("out of pages, ending loop")
        still_pages = False
        
print(len(reviews))
print(reviews[0])
