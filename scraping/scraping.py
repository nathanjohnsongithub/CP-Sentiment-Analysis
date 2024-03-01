import googlemaps

# Replace 'YOUR_API_KEY' with the actual API key you obtained
api_key = 'YOUR_API_KEY'
gmaps = googlemaps.Client(key=api_key)

# Specify the place_id for the location you are interested in
place_id = 'PLACE_ID'

# Fetch the details for the specified place
place_details = gmaps.place(place_id=place_id)

# Extract reviews
reviews = place_details['result']['reviews']

# Print the reviews
for review in reviews:
    print(f"Author: {review['author_name']}")
    print(f"Rating: {review['rating']}")
    print(f"Text: {review['text']}")
    print("\n")
