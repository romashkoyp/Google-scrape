# Code creates links for Google Search in CSV format to put it into service Google Search Results Scraper on apify.com
# and get result in JSON from Google Search Results Scraper
# idea is to integrate periods for each query in link
# code allows to get links with step from 2 days and more
# it helps to avoid Googles limitations and don't miss any results

from datetime import datetime, timedelta
import pandas as pd
from urllib.parse import quote

CSV_OUTPUT = r'C:\Users\romas\Documents\Code\Google scrape\result\links_for_google2.csv'

base_url = "https://www.google.com/search?q=allintext%3A++{word1}+OR+{word2}+OR+{word3}+%22{phrase1}+{phrase2}+{phrase3}%22+site%3A.ru&lr=lang_ru&cr=countryRU&sca_esv=589078860&hl=en&as_qdr=all&tbs=lr%3Alang_1ru%2Cctr%3AcountryRU%2Ccdr%3A1%2Ccd_min%3A{since_date}%2Ccd_max%3A{until_date}&sxsrf=AM9HkKnYAA2XA0cO2Mq9WYzBtY_0GhxLzQ%3A1702039480539&ei=uA9zZbuwILC_wPAPr5WvkAY&ved=0ahUKEwi77IWV7_-CAxWwHxAIHa_KC2IQ4dUDCBA&oq=allintext%3A++%D1%84%D0%B8%D0%BD%D0%BB%D1%8F%D0%BD%D0%B4%D0%B8%D1%8F+OR+%D1%84%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B9+OR+%D1%84%D0%B8%D0%BD%D0%BD%D1%8B+%22%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9+%D0%BC%D0%B8%D1%80%22+site%3A.ru&gs_lp=Egxnd3Mtd2l6LXNlcnAiX2FsbGludGV4dDogINGE0LjQvdC70Y_QvdC00LjRjyBPUiDRhNC40L3RgdC60LjQuSBPUiDRhNC40L3QvdGLICLRgNGD0YHRgdC60LjQuSDQvNC40YAiIHNpdGU6LnJ1SABQAFgAcAB4AJABAJgBAKABAKoBALgBDMgBAPgBAeIDBBgAIEE&sclient=gws-wiz-serp#ip=1"
links = []
start_date = datetime(2019, 1, 1)
end_date = datetime(2023, 12, 12)

def encode_cyrillic_to_hex(input_text):
    encoded_text = quote(input_text, encoding='utf-8-sig')
    return encoded_text

# Translate cyrillic words to hex
cyrillic_word1 = "финляндия"
word1 = encode_cyrillic_to_hex(cyrillic_word1)

cyrillic_word2 = "финский"
word2 = encode_cyrillic_to_hex(cyrillic_word2)

cyrillic_word3 = "финны"
word3 = encode_cyrillic_to_hex(cyrillic_word3)

cyrillic_phrase1 = "всемирный"
phrase1 = encode_cyrillic_to_hex(cyrillic_phrase1)

cyrillic_phrase2 = "конгресс"
phrase2 = encode_cyrillic_to_hex(cyrillic_phrase2)

cyrillic_phrase3 = "соотечественников"
phrase3 = encode_cyrillic_to_hex(cyrillic_phrase3)

# Generate links with a step of x days
while start_date <= end_date:
    since_date = start_date.strftime("%m/%d/%Y").lstrip("0").replace("/0", "%2F").replace("/", "%2F")  # Adjusted format using string manipulation
    until_date = min((start_date + timedelta(days=100)), end_date).strftime("%m/%d/%Y").lstrip("0").replace("/", "%2F")  # Adjusted format using string manipulation
    search_link = base_url.format(until_date=until_date, since_date=since_date, word1=word1, word2=word2, word3=word3, phrase1=phrase1, phrase2=phrase2, phrase3=phrase3)
    links.append([since_date, until_date, search_link])
    start_date += timedelta(days=101)

df = pd.DataFrame(links, columns=['since', 'until', 'link'])

# Make replacements only in the DataFrame after the while loop
df['since'] = df['since'].str.replace("%2F", "/")
df['until'] = df['until'].str.replace("%2F", "/")

# Save the DataFrame to a CSV file
df.to_csv(CSV_OUTPUT)
print(f"Data has been saved to {CSV_OUTPUT}\n")