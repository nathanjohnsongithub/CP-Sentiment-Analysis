# Scraping for yelp using BeautifulSoup and requests

# imports used
import re
import requests
from bs4 import BeautifulSoup

# Method to Scrap all of the reviews from a given yelp url.
def get_yelp_reviews(url: str, stop_early: bool) -> list:

    # If the user wants to stop early. Ask how many reviews they would like
    if stop_early:
        max_reviews = int(input('How many reviews would you like (Rounded up by ten)? '))

    # Get the length of the url which we would use for splicing later.
    original_url_length = len(url)
    # Initialize list with the reviews for the return variable.
    reviews = []
    # Initialize the counter, and still_pages for the while loop 
    counter = 0
    still_pages = True
    # Initialize the regex which will scan 
    # the soup file for all of the reviews.
    regex = re.compile('.*comment.*')
    # Keep looping until theyre no more pages to scrap or, 
    # the user specified max amount of reviews was reached. 
    while still_pages:
        # If the user wants to stop early and we've reached the maximum reviews.
        if (stop_early and counter > max_reviews):
            # Break the while loop
            still_pages = False
        # Make the soup to pull everything off that webpage.
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        # Pull all of the reviews using regex.
        results = soup.find_all('p', {'class':regex})
        # If there are no reviews inside of results we know its out of pages.
        if not results:
            still_pages = False
        # Take text values from each review and put it into a list.
        new_reviews = [result.text for result in results]
        # Add the new reviews into the reviews array
        reviews.extend(new_reviews)
        # Increment the counter by 10 which will "change the page" for yelp.
        counter += 10
        print(f'Page scraped. URL: {url}')
        # Update the url.
        url = f"{url[:original_url_length]}{'?start='}{counter}"
    # Return all of the reviews
    return reviews
        

# Sample use
all_reviews = get_yelp_reviews('https://www.yelp.com/biz/buffalo-joes-evanston', True)
print(len(all_reviews))
print(f"First review: {all_reviews[0]}")
print('')
print(f"Last  review: {all_reviews[len(all_reviews)-1]}")