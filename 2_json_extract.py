# Code gets result in JSON from Google Search Results Scraper
# Checks the desired results for duplicates and if any conditions were missed by Google Search Results Scraper
# Save result in CSV

import json
import csv

# Specify the path to JSON file and to output CSV file
json_input = r'C:\Users\romas\Documents\Code\Google scrape\result\dataset_google-search-scraper_2023-12-12_09-08-53-886.json'
csv_output = r'C:\Users\romas\Documents\Code\Google scrape\google_dataset_2.csv'

# Load JSON data from the file
with open(json_input, 'r', encoding='utf-8-sig') as file:
    data = json.load(file)

# Extract information from each entry in the JSON data
extracted_data = []

# Create a set to store unique URLs
unique_urls = set()

# Create a set to store date
current_date = []

id = 1564

for entry in data:
    search_query = entry.get("searchQuery", {}).get("term", "")
    for result in entry.get("organicResults", []):
        title = result.get("title", "")
        url = result.get("url", "")
        date = result.get("date", "")
        keywords = ', '.join(result.get("emphasizedKeywords", []))
        lower_keywords = keywords.lower()
        row_id = id

        # Remove leading and trailing symbols
        if url.startswith((",")) and url.endswith((",")):
            url = url[1:-1]
        
        # Remove leading prefixes
        if url.startswith("https://www."):
            domain = url.replace("https://www.", "")
        elif url.startswith("http://www."):
            domain = url.replace("http://www.", "")
        elif url.startswith("https://"):
            domain = url.replace("https://", "")
        elif url.startswith("http://"):
            domain = url.replace("http://", "")

        # Remove part of link after /
        if "/" in domain:
            domain = domain.split("/", 1)[0]

        # Check date
        if current_date and not date:
            date = current_date[-1]

        # Check the condition in keywords
        if ("финляндия" not in lower_keywords or "финский" not in lower_keywords or "финны" not in lower_keywords) and "русский мир" not in lower_keywords and not url.endswith(".pdf"):
            if url not in unique_urls:
                extracted_data.append({            
                    "query": search_query,
                    "title": title,
                    "url": url,
                    "domain": domain,
                    "date": date,
                    "keywords": keywords,
                    "id": row_id
                })
                # Add the URL to the set of unique URLs
                unique_urls.add(url)

                # Add date to the list
                current_date.append(date)

                # Update id
                id += 1

# Save extracted information to a CSV file
headers = ["query", "title", "url", "domain", "date", "keywords", "id"]

with open(csv_output, 'w', newline='', encoding='utf-8-sig') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=headers)

    # Write the header row
    writer.writeheader()

    # Write the data rows
    writer.writerows(extracted_data)

print(f"Data has been extracted and saved to {csv_output}.")