import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
 
# List of XML URLs to download
urls = [
    "https://assets.immoweb.be/sitemap/classifieds-000.xml",
    "https://assets.immoweb.be/sitemap/classifieds-001.xml",
    "https://assets.immoweb.be/sitemap/classifieds-002.xml",
    "https://assets.immoweb.be/sitemap/classifieds-003.xml",
    "https://assets.immoweb.be/sitemap/classifieds-004.xml",
    "https://assets.immoweb.be/sitemap/classifieds-005.xml",
    "https://assets.immoweb.be/sitemap/classifieds-006.xml",
    "https://assets.immoweb.be/sitemap/classifieds-007.xml",
    "https://assets.immoweb.be/sitemap/classifieds-008.xml",
    "https://assets.immoweb.be/sitemap/classifieds-009.xml",
    "https://assets.immoweb.be/sitemap/classifieds-010.xml",
    "https://assets.immoweb.be/sitemap/classifieds-011.xml",
    "https://assets.immoweb.be/sitemap/classifieds-012.xml",
    "https://assets.immoweb.be/sitemap/classifieds-013.xml",
    "https://assets.immoweb.be/sitemap/classifieds-014.xml",
    "https://assets.immoweb.be/sitemap/classifieds-015.xml",
    "https://assets.immoweb.be/sitemap/classifieds-016.xml",
    "https://assets.immoweb.be/sitemap/classifieds-017.xml",
    "https://assets.immoweb.be/sitemap/classifieds-018.xml",
    "https://assets.immoweb.be/sitemap/classifieds-019.xml",
    "https://assets.immoweb.be/sitemap/classifieds-020.xml",
    "https://assets.immoweb.be/sitemap/classifieds-021.xml",
    "https://assets.immoweb.be/sitemap/classifieds-022.xml",
    "https://assets.immoweb.be/sitemap/classifieds-023.xml",
    "https://assets.immoweb.be/sitemap/classifieds-024.xml",
    "https://assets.immoweb.be/sitemap/classifieds-025.xml",
    "https://assets.immoweb.be/sitemap/classifieds-026.xml",
    "https://assets.immoweb.be/sitemap/classifieds-027.xml",
    "https://assets.immoweb.be/sitemap/classifieds-028.xml",
    "https://assets.immoweb.be/sitemap/classifieds-029.xml",
    "https://assets.immoweb.be/sitemap/cms-000.xml",
    "https://assets.immoweb.be/sitemap/customers-000.xml",
    "https://assets.immoweb.be/sitemap/static-000.xml",
    "https://assets.immoweb.be/sitemap/static-001.xml",
    "https://assets.immoweb.be/sitemap/static-002.xml",
    "https://assets.immoweb.be/sitemap/static-003.xml",
    "https://assets.immoweb.be/sitemap/static-004.xml",
]
 
# Directory to save XML files
os.makedirs('xml_files', exist_ok=True)
 
all_urls = []
 
# Download and parse each XML file
for url in urls:
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        file_path = os.path.join('xml_files', url.split('/')[-1])
 
        # Save the XML file
        with open(file_path, 'wb') as file:
            file.write(response.content)
 
        # Parse the XML file
        soup = BeautifulSoup(response.content, 'xml')
 
        # Extract URLs (adjust the tag name based on the XML structure)
        loc_tags = soup.find_all('loc')
        for loc in loc_tags:
            all_urls.append(loc.text)
 
    except Exception as e:
        print(f"Error downloading or parsing {url}: {e}")
 
# Create a DataFrame and save to CSV
df = pd.DataFrame(all_urls, columns=['url'])
df.to_csv('xml_files/extracted_urls.csv', index=False)
 
 
###I have filtered the extracted urls (count = +900K) as a lot are duplicates in different languages. We only need appartments and houses for sale, so I filtered this. 
# You can choose your own preferences, just reshape the code below" preference, for example to extract the english content. 
# )
import pandas as pd
 
# Read the CSV file
df = pd.read_csv('extracted_urls.csv')
 
huis_pattern = 'https://www.immoweb.be/nl/zoekertje/huis/te-koop/'
appartement_pattern = 'https://www.immoweb.be/nl/zoekertje/appartement/te-koop/'
 
filtered_urls = df[df['url'].str.startswith(huis_pattern) | df['url'].str.startswith(appartement_pattern)]
 
# Output the matching URLs
print(filtered_urls)
 
filtered_urls.to_csv('filters.csv', index=False)