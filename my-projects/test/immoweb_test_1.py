import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import csv

# Step 1: Function to send request to the website with headers and cookies
def get_html_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        # Add other headers if needed
    }
    # Send GET request to the website
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Will raise an HTTPError if the response was an error
    return response.text

# Step 2: Function to extract all item URLs (houses and apartments) from the main page
def extract_item_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Extract all the <a> tags with listing URLs
    item_links = soup.find_all('a', href=True)
    
    urls = []
    for link in item_links:
        href = link['href']
        # Filter for valid property URLs (based on the site's URL structure)
        if '/en/classified/' in href:
            cleaned_url = re.sub(r'\?.*$', '', href)  # Clean URL from query parameters
            urls.append(cleaned_url)
    
    return list(set(urls))  # Remove duplicates

# Step 3: Function to save URLs to CSV
def save_urls_to_csv(urls, file_name='property_urls.csv'):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['URL'])  # Write header
        for url in urls:
            writer.writerow([url])

# Step 4: Function to load URLs from CSV
def load_urls_from_csv(file_name='property_urls.csv'):
    urls = []
    with open(file_name, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            urls.append(row[0])
    return urls

# Step 5: Function to extract data from individual property page
def extract_property_data(url):
    property_data = {
        'Property ID': None,
        'Locality': None,
        'Zip Code': None,
        'Price': None,
        'State of Property': None,
        'Number of Rooms': None,
        'Number of Baths': None,
        'Living Area Size': None,
        'Terrace Area Size': None,
        'Garden Area': None,
        'Swimming Pool': None,
        'Fire Place': None,
        'Kind of Property': None
    }

    html = get_html_data(url)
    soup = BeautifulSoup(html, 'html.parser')

    # Example extraction logic (you will need to inspect the site's HTML structure)
    try:
        property_data['Property ID'] = soup.find('span', {'class': 'property-id'}).text.strip() if soup.find('span', {'class': 'property-id'}) else 'None'
        property_data['Locality'] = soup.find('span', {'class': 'locality'}).text.strip() if soup.find('span', {'class': 'locality'}) else 'None'
        property_data['Zip Code'] = soup.find('span', {'class': 'zip-code'}).text.strip() if soup.find('span', {'class': 'zip-code'}) else 'None'
        property_data['Price'] = soup.find('span', {'class': 'price'}).text.strip() if soup.find('span', {'class': 'price'}) else 'None'
        property_data['State of Property'] = soup.find('span', {'class': 'property-state'}).text.strip() if soup.find('span', {'class': 'property-state'}) else 'None'
        property_data['Number of Rooms'] = soup.find('span', {'class': 'rooms'}).text.strip() if soup.find('span', {'class': 'rooms'}) else 'None'
        property_data['Number of Baths'] = soup.find('span', {'class': 'baths'}).text.strip() if soup.find('span', {'class': 'baths'}) else 'None'
        property_data['Living Area Size'] = soup.find('span', {'class': 'living-area'}).text.strip() if soup.find('span', {'class': 'living-area'}) else 'None'
        property_data['Terrace Area Size'] = soup.find('span', {'class': 'terrace-area'}).text.strip() if soup.find('span', {'class': 'terrace-area'}) else 'None'
        property_data['Garden Area'] = soup.find('span', {'class': 'garden-area'}).text.strip() if soup.find('span', {'class': 'garden-area'}) else 'None'
        property_data['Swimming Pool'] = soup.find('span', {'class': 'swimming-pool'}).text.strip() if soup.find('span', {'class': 'swimming-pool'}) else 'None'
        property_data['Fire Place'] = soup.find('span', {'class': 'fire-place'}).text.strip() if soup.find('span', {'class': 'fire-place'}) else 'None'
        property_data['Kind of Property'] = soup.find('span', {'class': 'property-kind'}).text.strip() if soup.find('span', {'class': 'property-kind'}) else 'None'
    except Exception as e:
        print(f"Error extracting data from {url}: {e}")
    
    return property_data

# Step 6: Function to save extracted data to Excel
def save_data_to_excel(data, file_name='property_data.xlsx'):
    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False)

# Main function to execute the whole process
def main():
    base_url = 'https://www.immoweb.be/en'
    
    # Step 1: Get the HTML data from the main page
    html_data = get_html_data(base_url)

    # Step 2: Extract URLs for houses and apartments for sale
    urls = extract_item_urls(html_data)

    # Step 3: Save these URLs to a CSV file
    save_urls_to_csv(urls)

    # Step 4: Load URLs from the CSV
    urls = load_urls_from_csv()

    # Step 5: Extract property data from each URL
    all_property_data = []
    for url in urls:
        property_data = extract_property_data(url)
        all_property_data.append(property_data)

    # Step 6: Save all extracted property data to an Excel file
    save_data_to_excel(all_property_data)

# Uncomment the following line to run the main function
# main()
