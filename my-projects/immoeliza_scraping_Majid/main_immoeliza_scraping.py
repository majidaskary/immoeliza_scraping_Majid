# immoeliza scraping project

import requests
from bs4 import BeautifulSoup  
from lxml import html
import csv


# immoweb house and apartment fore sale's page
immoweb_sale_link = 'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page=1&orderBy=relevance'

   

# for fixing  error 403
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# it use to manage cookies
session = requests.Session()

# to extract the links from group pages
response_group_page = session.get(immoweb_sale_link, headers=headers)

soup = BeautifulSoup(response_group_page.text, 'html.parser')

if response_group_page.status_code == 200:
    print("well done, passed for group page") 
    #print(soup.prettify()) 
else:
    print(response_group_page.status_code)


# ---------------------------------------------------------------------------------------------------
# generating the links of 333 pages 

first_group_pages_link_sale = 'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&amp%3BorderBy=relevance&amp%3Bpage=2'
p = 1
last_p = 333
group_pages_link_sale = []

# adding 1st page in 1st cell of list
group_pages_link_sale.append(first_group_pages_link_sale)

for p in range(2,last_p+1):  
    group_pages_link_sale.append(first_group_pages_link_sale +"&page=" + str(p))   # adding the link + new number of pages

#group_pages_link_sale

# ---------------------------------------------------------------------------------------------------
# extracting all linkes (+10000 links) for sale from immoweb// by group_pages_link_sale

all_links = []              

#group_pages_link_sale_test = group_pages_link_sale[:2]

for l in group_pages_link_sale:#_test:          # a loop to scrape that 333 group pages of immoweb

    session = requests.Session()               
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = session.get(l, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for tag_a in soup.find_all('a', class_="card__title-link", href=True):   # extracting all item links paer group page
        all_links.append(tag_a['href'])

#all_links 

# ---------------------------------------------------------------------------------------------------
# save all the links in a csv file:

with open("all_linkes.csv",mode="w",newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(all_links)  

# ---------------------------------------------------------------------------------------------------
# extracting 2 item frpm all links, Peroperty ID and Price
data_set_immoweb = []

for counter in range(len(all_links)):
    
    counter_row = all_links[counter]
    #print(counter_row)
    session = requests.Session()               
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = session.get(counter_row, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    property_id_div = soup.find('div', 'classified__header--immoweb-code')   # Find the div containing the property ID
    property_id = (property_id_div).text.strip().split(': ')[-1]             # Extract the text and split it to get the ID
    #print(f'1.property ID :  {property_id}')

    #  4. Price
    price_p = soup.find('p', 'classified__price')                         
    price = price_p.find('span', {'aria-hidden': 'true'}).text.strip()    
    #print(f'4.price :  {price}')  
    #data_set_immoweb_test [counter,0] = counter
    #data_set_immoweb_test [counter,1] = price
    data_set_immoweb.append([counter_row, property_id, price])

#data_set_immoweb   

# ---------------------------------------------------------------------------------------------------
# save all the data in a csv file:

with open("all_data.csv",mode="w",newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(data_set_immoweb) 
