# Scraping for yelp using BeautifulSoup and requests

# imports used
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# Method to Scrap all of the reviews from a given yelp url.
def get_yelp_reviews(url: str, stop_early: bool) -> tuple:

    # If the user wants to stop early. Ask how many reviews they would like
    if stop_early:
        max_reviews = int(input('How many reviews would you like (Rounded up by ten)? '))

    # Get the length of the url which we would use for splicing later.
    original_url_length = len(url)
    # Initialize list with the reviews for the return variable.
    reviews = []
    ratings = []
    # Initialize the counter, and still_pages for the while loop 
    counter = 0
    still_pages = True
    # Initialize the regegs which will scan the soup file 
    # for all of the reviews and star ratings.
    regex_reviews = re.compile('.*comment.*')
    regex_ratings = re.compile('css-14g69b3')

    # Keep looping until theyre no more pages to scrap or, 
    # the user specified max amount of reviews was reached. 
    while still_pages:
        # If the user wants to stop early and we've reached the maximum reviews.
        if (stop_early and counter > max_reviews):
            # Break the while loop
            still_pages = False

        # Make the soup to pull everything off that webpage.
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        # Now scrap everything from only the reviews section. that is the 'list__...'
        html_reviews = soup.find_all('ul', class_='list__09f24__ynIEd')
        # Now turn that html_reviews into another soup object so we can
        # scrap with regex. converting the reviews section into a string.
        partial_soup = BeautifulSoup(str(html_reviews), "html.parser")

        # Pull all of the reviews and ratings using regex.
        results_reviews = partial_soup.find_all('p', {'class':regex_reviews})
        ratings_ratings = partial_soup.find_all('div', {'class':regex_ratings})

        # If there are no reviews inside of results we know its out of pages.
        if not results_reviews:
            still_pages = False

        # Take text values from each review or rating and put it into a list.
        new_reviews = [result.text for result in results_reviews]
        new_ratings = [result.get('aria-label') for result in ratings_ratings]
        # Add the new reviews into the reviews array
        reviews.extend(new_reviews)
        ratings.extend(new_ratings)
        
        # Increment the counter by 10 which will "change the page" for yelp.
        counter += 10
        print(f'Page scraped. URL: {url}')
        # Update the url.
        url = f"{url[:original_url_length]}{'?start='}{counter}"
    # Return all of the reviews
    return (reviews, ratings)
    # return pd.DataFrame({'review': reviews, 'rating': ratings})
        

# Sample use
# df = get_yelp_reviews('https://www.yelp.com/biz/buffalo-joes-evanston', True)
# print(len(all_reviews))
# print(f"First review: {all_reviews[0]}")
# print('')
# print(f"Last  review: {all_reviews[len(all_reviews)-1]}")

# print(df.shape)
# print(df.head)