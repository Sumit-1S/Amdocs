import requests
from bs4 import BeautifulSoup
from googlesearch import search  # Ensure you have the googlesearch-python package installed
import json

def google_search(query, num_results=1):
    """
    Perform a Google search and return the first `num_results` URLs.
    """
    try:
        search_results = list(search(query, num_results=num_results, lang='en'))
        return search_results
    except Exception as e:
        print(f"Error during Google search: {e}")
        return []

def fetch_article_text(url, class_name, word_limit=4000):
    """
    Fetch the article from the given URL and extract text from the specified class,
    limiting the extracted content to a specified number of words.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        article_div = soup.find('div', class_=class_name)
        if article_div:
            paragraphs = article_div.find_all('p')
            word_count = 0
            text_chunks = []
            for para in paragraphs:
                para_text = para.get_text(separator=' ', strip=True)
                words = para_text.split()
                current_word_count = len(words)
                if word_count + current_word_count > word_limit:
                    remaining_words = word_limit - word_count
                    text_chunks.append(" ".join(words[:remaining_words]))
                    break
                else:
                    text_chunks.append(para_text)
                    word_count += current_word_count
            return " ".join(text_chunks)
        else:
            print(f"No div with class '{class_name}' found in {url}")
            return ""
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
        return ""


def chunk_text(text, chunk_size=2000, overlap=20):
    """
    Split the text into chunks of approximately `chunk_size` words with an `overlap` between chunks.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
    return chunks

def main():
    # Define the base search query
    base_query = "budget 2025 Nirmala Sitharaman income tax announcements"
    
    # Define the news outlets and their corresponding class names
    news_outlets = {
        #"Times of India": "js_tbl_article",
        #"The Hindu": "articlebodycontent",
        "NDTV": "Art-exp_cn"
    }
    
    # Dictionary to store the extracted content
    content_data = {}
    
    # Loop through each news outlet
    for outlet, class_name in news_outlets.items():
        # Create the search query by appending the outlet name
        search_query = f"{base_query} {outlet}"
        print(f"Searching for: {search_query}")
        
        # Perform the search and get the first result
        urls = google_search(search_query, num_results=1)
        if urls:
            url = urls[0]
            print(f"Fetching article from: {url}")
            # Fetch the article text
            article_text = fetch_article_text(url, class_name)
            if article_text:
                # Chunk the article text
                chunks = chunk_text(article_text)
                content_data[outlet] = {
                    "url": url,
                    "chunks": chunks
                }
            else:
                print(f"Failed to extract content from {url}")
        else:
            print(f"No search results found for {search_query}")
    
    # Optionally, save the content data to a JSON file
    with open("extracted_content.json", "w", encoding="utf-8") as f:
        json.dump(content_data, f, indent=4, ensure_ascii=False)
    
    # Print the extracted content data
    print("\nExtracted Content Data:")
    print(json.dumps(content_data, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
