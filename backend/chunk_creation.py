import requests
import ssl
import nltk
import os
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

# Fix SSL certificate verification issues
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download required NLTK data with verification
def download_nltk_data():
    nltk_download_dir = os.path.join(os.path.expanduser("~"), "nltk_data")
    
    if not os.path.exists(nltk_download_dir):
        os.makedirs(nltk_download_dir)
    
    # List of required NLTK resources
    required_resources = ['punkt', 'stopwords', 'punkt_tab']
    for resource in required_resources:
        try:
            if resource == 'punkt_tab':
                nltk.data.find(f'tokenizers/{resource}')
            else:
                nltk.data.find(resource)
        except LookupError:
            nltk.download(resource, download_dir=nltk_download_dir, quiet=True)

# Run the download function first
download_nltk_data()

def get_article_title(url):
    """
    Fetch the article title from the given URL.
    This implementation uses requests and BeautifulSoup to extract text from the <title> tag.
    If the <title> tag is missing, it attempts to use an <h1> tag.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text().strip()
        # Fallback: Try to find an <h1> tag if <title> is not present
        h1_tag = soup.find('h1')
        if h1_tag:
            return h1_tag.get_text().strip()
        return ""
    except Exception as e:
        print(f"Error fetching article title: {e}")
        return ""

def extract_keywords_from_title(title):
    """
    Extract keywords from the article title by tokenizing the title text,
    and filtering out common stopwords and non-alphabetic tokens.
    """
    tokens = nltk.word_tokenize(title)
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in tokens if word.lower() not in stop_words and word.isalpha()]
    return keywords

def process_article_url(url):
    """
    Process the article URL by first fetching its title and then extracting keywords from that title.
    """
    title = get_article_title(url)
    if not title:
        return []
    keywords = extract_keywords_from_title(title)
    return keywords

if __name__ == "__main__":
    article_url = "https://timesofindia.indiatimes.com/business/india-business/budget-2025-live-updates-income-tax-slabs-nirmala-sitharaman-speech-highlights-announcements-union-budget-2025/liveblog/117801000.cms"  # Replace with actual URL if needed
    keywords = process_article_url(article_url)
    print("Extracted Keywords from Article Title:")
    print(keywords)
