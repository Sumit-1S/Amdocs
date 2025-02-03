from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import chunk_creation
import web_scraper
import requests
import os
from openai import OpenAI
import re

app = Flask(__name__)
CORS(app) 
load_dotenv()
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"  
OPENAI_API_KEY = os.getenv('OPENAI_API')
collected_data=[]

@app.route('/', methods=['GET'])
def home():
    return "Server running successfully"

@app.route('/process', methods=['POST'])
def process_article():
    data = request.get_json()
    article_link = data.get('article_link')

    if not article_link:
        return jsonify({"error": "Missing 'article_link'"}), 400

   
    client = OpenAI()
    add_text= "Take this article link and create an array of keywords which are relevant to the article. The array should contain 5 key hrases which are each of 2-3 word length and should be relevant to the article header. return me only the array of keywords. nothing else "
    
    chunk_prompt = (f"{article_link} {add_text}")
    
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": chunk_prompt}
    ])
    
    message_content = completion.choices[0].message.content
    json_content = re.sub(r'^```json\n|```$', '', message_content.strip())

    # Now, 'json_content' should be a clean JSON string
    keywords = json_content.split(",")
    keywords = [kw.strip() for kw in keywords if kw]

    # Evaluate credibility score and source reliability
    top_news_channels = ["indiatoday", "timesofindia", "hindustantimes", "zeenews", "ndtv", "thehindu"]
    mid_news_channels = ["news18", "indianexpress", "republicworld", "firstpost", "scroll", "theprint"]
    low_news_channels = ["opindia", "swarajyamag", "siasat", "thequint", "thewire", "newslaundry"]
    
    credibility_score, source_reliability, collected_data = web_scraper.evaluate_chunks(keywords)
    
    article_link = article_link.removeprefix("https://")
    news_outlet = article_link.split(".")[0]
    
    if news_outlet in top_news_channels:
        source_reliability = 100
    elif news_outlet in mid_news_channels:
        source_reliability = 50
    elif news_outlet in low_news_channels:
        source_reliability = 30
    else:
        source_reliability = 0
    
    response = {
        "credibilityScore": credibility_score,
        "reliabilityScore": source_reliability,
    }
  
    print(response)
    return response

@app.route('/chat', methods=['POST'])
def talk():
    data = request.get_json()
    input_query = data.get('input_query')

    if not input_query:
        return jsonify({"error": "Missing 'input_query'"}), 400

    client = OpenAI()
    genai_prompt = "Take this info and store it. Don't return anything for now."
    messages = [{"role": "system", "content": "You are a helpful assistant that remembers previous inputs."}]
    
    for chunk in collected_data:
        new_prompt = f"{chunk} {genai_prompt}"
        messages.append({"role": "user", "content": new_prompt})
        
    messages.append({"role": "user", "content": genai_prompt})
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    response = completion.choices[0].message.content
    print(response)
    return response
    

if __name__ == '__main__':
    app.run(port=5000)
