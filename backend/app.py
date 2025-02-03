from flask import Flask, request, jsonify
from flask_cors import CORS
import chunk_creation
import web_scraper
import requests
from openai import OpenAI

app = Flask(__name__)
CORS(app)  

OPENAI_API_URL = "https://api.perplexity.ai/v1/complete"  
OPENAI_API_KEY = "your_api_key_here"

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
    
    keywords = completion.choices[0].message.content.strip().split(",")
    keywords = [kw.strip() for kw in keywords if kw]
    print(keywords)

    # Evaluate credibility score and source reliability
    credibility_score, source_reliability, collected_data = web_scraper.evaluate_chunks(keywords)

    response = {
        "credibilityScore": credibility_score,
        "reliabilityScore": source_reliability,
    }
    
    genai_prompt = "Take this info and store it. Don't return anything for now."
    messages = [{"role": "system", "content": "You are a helpful assistant that remembers previous inputs."}]
    
    for chunk in collected_data:
        new_prompt = f"{chunk} {genai_prompt}"
        messages.append({"role": "user", "content": new_prompt})
        
        client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages  # Sends updated conversation history
        )
        
    print(response)
    return response

@app.route('/chat', methods=['POST'])
def talk(input_query):
    data = request.get_json()
    input_query = data.get('input_query')

    if not input_query:
        return jsonify({"error": "Missing 'input_query'"}), 400

    client = OpenAI()
    messages = [
        {"role": "system", "content": "You are a helpful assistant that remembers previous inputs."},
        {"role": "user", "content": input_query}
    ]
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    response = completion.choices[0].message.content
    print(response)
    return response
    

if __name__ == '__main__':
    app.run(port=5000)
