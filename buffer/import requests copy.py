import requests

import pprint

root_url = "https://country-leaders.onrender.com/"

endpoint = "status"

#params- (

# "apiKey": "73bbb95f8ecb49b499113a46481b4af1

# "sources": "lequipe"

#call the get method of requests on our specifications

response requests.get(

f"{root_url}/{endpoint)"

#params-params

)

data response.json()

articles data.get('articles', ()) # Get the list of articles (or an empty list if 'articles' doesn't ex

titles[]#Create an empty list to store the titles

#Loop through each article in the list

for article in articles:

titles.append(article['title']) # Add the article's title to the titles list

#Now, titles contains the titles of all the articles

pprint.pp(titles)