import requests
from bs4 import BeautifulSoup

def fetch_article_title(url):
    """
    Fetch the article from the given URL and extract the title.
    Returns the title text if available, otherwise an empty string.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
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

def process_article_url(article_url):
    """
    Fetch the article title and create chunks from it.
    """
    title = fetch_article_title(article_url)
    if not title:
        print("Failed to retrieve the article title.")
        return []
    chunks = chunk_text(title)
    return chunks

def main():
    article_url = "https://timesofindia.indiatimes.com/india/unblemished-track-record-fm-sitharaman-on-why-moodys-has-not-changed-indias-ranking/articleshow/117859152.cms"
    chunks = process_article_url(article_url)
    
    for chunk in chunks:
        print(chunk)
        
if __name__ == '__main__':
    main()        