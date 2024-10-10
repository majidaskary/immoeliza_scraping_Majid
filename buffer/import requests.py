import requests
#from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/Shapur_II'
response = requests.get(url)


print('Type: \n', response.text)


