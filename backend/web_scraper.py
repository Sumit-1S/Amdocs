import requests
import json
from bs4 import BeautifulSoup
from googlesearch import search  # pip install googlesearch-python

def google_search(query, num_results=3):
    """
    Use the googlesearch module to fetch the first `num_results` URLs for the given query.
    """
    results = []
    try:
        for url in search(query, num_results=num_results, lang='en'):
            results.append(url)
    except Exception as e:
        print(f"Error during Google search: {e}")
    return results

def fetch_article_text(url):
    """
    Fetch the article from the given URL and extract plain text from all <p> tags.
    This function uses BeautifulSoup to strip away any embedded HTML and joins the text with a space.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        # For each paragraph, extract the text using a space as a separator and remove extra whitespace.
        text = " ".join([para.get_text(separator=' ', strip=True) 
                         for para in paragraphs if para.get_text(strip=True)])
        return text
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
        return ""

def main():
    # Define your tags (keywords)
    tags = ["budget", "2025", "Nirmala Sitharaman", "income tax", "announcements"]
    search_query = " ".join(tags)
    print("Search Query:", search_query)
    
    # Get the first three search URLs
    urls = google_search(search_query, num_results=1)
    print("\nFetched URLs:")
    for idx, url in enumerate(urls, 1):
        print(f"{idx}. {url}")
    
    # Dictionary to store the plain text content from each URL
    data = {}
    for url in urls:
        article_text = fetch_article_text(url)
        if article_text:
            data[url] = article_text
        else:
            print(f"No article text found for URL: {url}")
    
    # Convert the dictionary to JSON text
    json_data = json.dumps(data, indent=4)
    
    # Print the JSON data for debugging purposes
    print("\nJSON Data from search results:")
    print(json_data)
    
    # Optionally, save the JSON data to a file
    with open("search_results.json", "w", encoding="utf-8") as f:
        f.write(json_data)

if __name__ == "__main__":
    main()
