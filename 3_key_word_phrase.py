# Code gets as input urls for checking again, but directly on each website
# for desired keywords and key phrases in text
# result comes as CSV file with ID of TXT file which is extracted from each webpage separetely

import requests
from bs4 import BeautifulSoup
import re
import csv
from concurrent.futures import ThreadPoolExecutor
import threading
import os

# Define global variables for input and output files
CSV_INPUT = r'C:\Users\romas\Documents\Code\Google scrape\google_dataset_2.csv' # Path to source csv file
CSV_OUTPUT = r'C:\Users\romas\Documents\Code\Google scrape\result_txt_2\google_dataset_checked_2.csv' # Path to where is saved new csv file with result
TXT_OUTPUT_FOLDER = r'C:\Users\romas\Documents\Code\Google scrape\result_txt_2' # Path to save new txt files with texts from webpages

# Ensure that the output folder exists; create it if not
os.makedirs(TXT_OUTPUT_FOLDER, exist_ok=True)

# Define a lock for file writing
FILE_WRITE_LOCK = threading.Lock()

# Function to extract keywords from a webpage
def extract_keywords(url):
    
    try:
        # Send a GET request to the webpage
        response = requests.get(url, timeout=4)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the webpage
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract text content
            text_content = soup.get_text()
            
            # Split text into sentences
            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text_content)
            
            # Define a list of keywords you want to detect
            keywords_to_detect = [
                r'\bфинляндия\b', r'\bфинляндию\b', r'\bфинляндии\b', r'\bфинляндей\b',
                r'\bфинский\b', r'\bфинского\b', r'\bфинскому\b', r'\bфинским\b', r'\bфинском\b',
                r'\bфинская\b', r'\bфинской\b', r'\bфинскую\b', r'\bфинское\b', 
                r'\bфинские\b', r'\bфинских\b', r'\bфинским\b', r'\bфинскими\b',
                r'\bфинн\b', r'\bфинна\b', r'\bфинну\b', r'\bфинном\b', r'\bфинне\b', 
                r'\bфинка\b', r'\bфинки\b', r'\bфинке\b', r'\bфинку\b', r'\bфинкой\b',
                r'\bфинок\b', r'\bфинкам\b', r'\bфинками\b', r'\bфинках\b',
                r'\bфинны\b', r'\bфиннов\b', r'\bфиннам\b', r'\bфиннами\b', r'\bфиннах\b'
            ]
            
            # Define a list of keyphrases you want to detect
            keyphrases_to_detect = [
                r'\bрусский мир\b', r'\bрусского мира\b', r'\bрусскому миру\b', r'\bрусским миром\b', r'\bрусском мире\b'
            ]
                
            # Counter for sentences that meet the conditions
            count_keyword = 0
            count_keyphrase = 0

            # Initialize variables to store detected keyword and keyphrase
            detected_keyword = None
            detected_keyphrase = None

            # Iterate through sentences to find and print the detected keywords or keyphrases along with the whole sentence
            for sentence in sentences:
                keyword_detected = any(re.search(keyword, sentence, re.IGNORECASE) for keyword in keywords_to_detect)
                keyphrase_detected = any(re.search(phrase, sentence, re.IGNORECASE) for phrase in keyphrases_to_detect)

                # Clean the sentence
                cleaned_sentence = ' '.join(sentence.split())

                # Check if any word in the cleaned sentence has length greater than 20
                long_word_present = any(len(word) > 20 for word in cleaned_sentence.split())

                if not long_word_present:
                    if count_keyword < 1:
                        if keyword_detected:
                            count_keyword += 1
                            detected_keyword = next(keyword for keyword in keywords_to_detect if re.search(keyword, sentence, re.IGNORECASE))
                    elif count_keyphrase < 1:
                        if keyphrase_detected:
                            count_keyphrase += 1
                            detected_keyphrase = next(phrase for phrase in keyphrases_to_detect if re.search(phrase, sentence, re.IGNORECASE))
            
            # Remove 2 first and 2 last characters from keyword and keyphrase
            if detected_keyword:
                detected_keyword = detected_keyword[2:-2]
            if detected_keyphrase:
                detected_keyphrase = detected_keyphrase[2:-2]

            # Print the detected keyword and keyphrase
            print(f"Detected Keyword: {detected_keyword}")
            print(f"Detected Keyphrase: {detected_keyphrase}\n")

            # Return the detected keyword and keyphrase
            return detected_keyword, detected_keyphrase, text_content

        else:
            print(f"Failed to fetch content. Status code: {response.status_code}\n")

    except requests.exceptions.ConnectTimeout as e:
        print(f"Connection to {url} timed out. {e}\n")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}\n")
    except Exception as e:
        print(f"An unexpected error occurred: {e}\n")
    # Return None if extraction fails
    return None, None

def process_row(row):
    url = row["url"]
    detected_keyword, detected_keyphrase, text_content = extract_keywords(url)

    # Update the row with the detected keyword and keyphrase
    row["detected_keyword"] = detected_keyword
    row["detected_keyphrase"] = detected_keyphrase

    # Return the row if both keyword and keyphrase are found
    if detected_keyword is not None and detected_keyphrase is not None:
        # Create a filename based on the "id" from the CSV within the desired folder
        filename = os.path.join(TXT_OUTPUT_FOLDER, f"{row['id']}.txt")

        # Open a new file for the text content
        with open(filename, 'w', encoding='utf-8-sig') as txt:
            # Write the text content to the file
            txt.write(text_content)

            with open(CSV_OUTPUT, 'a', newline='', encoding='utf-8-sig') as output_csv:
                writer = csv.DictWriter(output_csv, fieldnames=headers)

                # Write the header row if the file is empty
                if output_csv.tell() == 0:
                    writer.writeheader()
                
                with FILE_WRITE_LOCK:
                    # Write the data row
                    writer.writerow(row)

    return None

# Read the original CSV
with open(CSV_INPUT, 'r', newline='', encoding='utf-8-sig') as input_csv:
    reader = csv.DictReader(input_csv)

    # Initialize the output CSV
    headers = ["query", "title", "url", "domain", "date", "keywords", "detected_keyword", "detected_keyphrase", "id"]

    with ThreadPoolExecutor() as executor:
        # Process each row concurrently
        executor.map(process_row, reader)

print(f"Data has been parsed and saved to {CSV_OUTPUT}.\n")
