import requests
from bs4 import BeautifulSoup
import re
import json

# Function to fetch a URL and parse the content
def fetch_url_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

# Function to extract file URLs from the page content
def extract_file_urls(content):
    file_urls = {
        'mp3': [],
        'images': [],
        'other_files': []
    }
    
    # Parsing HTML with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all anchor (<a>) tags that have href attribute
    links = soup.find_all('a', href=True)
    
    # Regex patterns for various file extensions
    mp3_pattern = r'\.mp3$'
    image_pattern = r'\.(jpg|jpeg|png|gif|bmp|svg|webp)$'
    other_files_pattern = r'\.(pdf|docx|xlsx|txt|zip|tar|rar|exe|pptx)$'

    # Process each link
    for link in links:
        href = link['href']
        
        if re.search(mp3_pattern, href, re.IGNORECASE):
            file_urls['mp3'].append(href)
        elif re.search(image_pattern, href, re.IGNORECASE):
            file_urls['images'].append(href)
        elif re.search(other_files_pattern, href, re.IGNORECASE):
            file_urls['other_files'].append(href)

    return file_urls

# Main function to process the URL and extract file links
def process_url(url):
    content = fetch_url_content(url)
    if content:
        file_urls = extract_file_urls(content)
        
        # Save the file URLs in a JSON file
        with open('file_urls.json', 'w') as json_file:
            json.dump(file_urls, json_file, indent=4)

        print("File URLs have been extracted and saved in 'file_urls.json'.")
    else:
        print("Failed to retrieve or parse the content of the URL.")

# Example usage
url = "https://example.com"  # Replace with the URL you want to scrape
process_url(url)
