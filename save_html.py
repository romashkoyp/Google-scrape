import requests
from bs4 import BeautifulSoup

def save_webpage_as_html(url, output_file):
    try:
        # Send a GET request to the webpage
        response = requests.get(url, timeout=10)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the webpage
            soup = BeautifulSoup(response.text, 'html.parser')

            # Get the text content
            text_content = soup.get_text()

            # Save the text content to an HTML file
            with open(output_file, 'w', encoding='utf-8') as html_file:
                html_file.write(text_content)

            print(f"Webpage content saved to {output_file}")

        else:
            print(f"Failed to fetch content. Status code: {response.status_code}")

    except requests.exceptions.ConnectTimeout as e:
        print(f"Connection to {url} timed out. {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
webpage_url = 'https://proza.ru/2019/02/04/1480'
output_html_file = 'webpage_content.txt'
save_webpage_as_html(webpage_url, output_html_file)
