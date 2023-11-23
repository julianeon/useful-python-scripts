import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    # Send a request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract and print the title of the page
        title = soup.title.string
        print("Title of the page:", title)

        # Extract and print the text of the first paragraph
        paragraph = soup.p.text
        print("First paragraph:", paragraph)
    else:
        print("Failed to retrieve the webpage")

if __name__ == "__main__":
    url = 'http://example.com'
    scrape_website(url)
