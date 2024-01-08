import requests
from bs4 import BeautifulSoup
import re

# Function to extract keywords from a webpage
def extract_keywords(url):
    # Send a GET request to the webpage
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text content from the HTML and split into sentences
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', soup.get_text())
        
        # Define a list of keywords you want to detect
        keywords_to_detect = [
    'финляндия', 'финляндию', 'финляндии', 'финляндей',
    'финский', 'финского', 'финскому', 'финским', 'финском',
    'финская', 'финской', 'финскую', 'финское', 
    'финские', 'финских', 'финским', 'финскими',
    'финн', 'финна', 'финну', 'финном', 'финне', 
    'финка', 'финки', 'финке', 'финку', 'финкой',
    'финок','финкам','финок','финками', 'финках',
    'финны', 'финнов', 'финнам', 'финнами', 'финнах'
    ]
        
        # Iterate through sentences to find and print the detected keywords along with the whole sentence
        for sentence in sentences:
            if any(keyword.lower() in sentence.lower() for keyword in keywords_to_detect):
                cleaned_sentence = ' '.join(sentence.split())
                print("Detected Keywords in Sentence:", cleaned_sentence)
    else:
        print("Failed to retrieve webpage. Status code:", response.status_code)

# Example usage
webpage_url = 'https://forum.guns.ru/forum_light_message/151/2578242.html'
extract_keywords(webpage_url)
