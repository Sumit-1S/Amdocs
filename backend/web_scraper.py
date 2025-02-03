import requests
from bs4 import BeautifulSoup
from googlesearch import search  # Ensure you have the googlesearch-python package installed
import json

def google_search(query, num_results=2):
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

def evaluate_chunks(chunks):
    """
    Evaluate each word in the chunks list by performing a Google search,
    fetching the article text, and calculating the credibility score.
    """
    credibility = 0
    num_queries = 0
    
    news_outlets = {
        #"Times of India": "js_tbl_article",
        #"The Hindu": "articlebodycontent",
        "NDTV": "Art-exp_cn"
    }

    # Dictionary to store the extracted content
    content_data = {}

    # Loop through each word in the chunks list
   # for word in chunks:
        # Perform the search and get the first result
    for outlet, class_name in news_outlets.items():
        # Create the search query by appending the outlet name
            search_query = f"{chunks} {outlet}"
            print(f"Searching for: {search_query}")
        
        # Perform the search and get the first result
            urls = google_search(search_query, num_results=1)
            if urls:
                url = urls[0]
                print(f"Fetching article from: {url}")
                # Fetch the article text
                article_text = fetch_article_text(url, class_name)
                if article_text:
                    content_data[outlet] = {
                        "url": url,
                        "chunks": chunks
                    }
                else:
                    print(f"Failed to extract content from {url}")
            else:
                print(f"No search results found for {search_query}")

    # Calculate credibility score
    credibility_score = (credibility / num_queries) * 100 if num_queries > 0 else 0
    reliability_score = 100  # As specified

    # Optionally, save the content data to a JSON file
    with open("extracted_content.json", "w", encoding="utf-8") as f:
        json.dump(content_data, f, indent=4, ensure_ascii=False)

    # Print the extracted content data
    print("\nExtracted Content Data:")
    print(json.dumps(content_data, indent=4, ensure_ascii=False))

    return credibility_score, reliability_score, content_data

