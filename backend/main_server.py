from flask import Flask, request, jsonify
import chunk_creation

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_article():
    """
    Expects a JSON payload with:
      - "article_link": URL of the article.
      - "user_query": A user query.
    
    It processes the article using chunk_creation.process_article_url() and returns a JSON
    object containing the user query and the extracted keyword chunks.
    """
    data = request.get_json()
    article_link = data.get('article_link')
    user_query = data.get('user_query')

    if not article_link or not user_query:
        return jsonify({"error": "Missing 'article_link' or 'user_query'"}), 400

    # Process the article to get keyword chunks
    chunks = chunk_creation.process_article_url(article_link)
    
    response = {
        "user_query": user_query,
        "chunks": chunks
    }
    return jsonify(response), 200

if __name__ == '__main__':
    # Start the server on port 3000
    app.run(port=3000)
