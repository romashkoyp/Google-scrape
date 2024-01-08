import requests
from bs4 import BeautifulSoup
import re

# Function to extract keyphrases from a webpage
def extract_keyphrases(url):
    # Send a GET request to the webpage
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text content from the HTML and split into sentences
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s*', soup.get_text())
        
        # Define a list of keyphrases you want to detect
        keyphrases_to_detect = [
            'русский мир', 'русского мира', 'русскому миру', 'русским миром', 'русском мире'
        ]
        
        # Iterate through sentences to find and print the detected keyphrases along with the whole sentence
        for sentence in sentences:
            if any(phrase.lower() in sentence.lower() for phrase in keyphrases_to_detect):
                # Remove leading and trailing whitespaces, including newline characters
                cleaned_sentence = ' '.join(sentence.split())
                print("Detected Keyphrases in Sentence:", cleaned_sentence)
    else:
        print("Failed to retrieve webpage. Status code:", response.status_code)

# Example usage
webpage_url = 'https://www.fontanka.ru/2019/02/24/005/'
extract_keyphrases(webpage_url)
