import requests
from bs4 import BeautifulSoup
import subprocess
import json

def fetch_article_title(url):
    """
    Fetch the article from the given URL and extract the title.
    Returns the title text if available, otherwise an empty string.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else ''
        return title.strip()
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
        return ""

def chunk_text(text, chunk_size=5):
    """
    Split the text into chunks of specified size.
    """
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def main():
    # Prompt the user for the article URL
    article_url = input("Enter the article URL: ").strip()
    
    # Fetch the article title
    title = fetch_article_title(article_url)
    if not title:
        print("Failed to retrieve the article title.")
        return
    
    # Create chunks from the title
    chunks = chunk_text(title)
    
    # Convert chunks to JSON string
    chunks_json = json.dumps(chunks)
    print(chunks)
    # Call web_scraper.py and pass the chunks as an argument
    try:
        result = subprocess.run(
            ['python', 'web_scraper.py', chunks_json],
            check=True,
            text=True,
            capture_output=True
        )
        print("web_scraper.py output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error calling web_scraper.py: {e}")

if __name__ == "__main__":
    main()
