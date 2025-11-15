from flask import Flask, request, render_template_string, jsonify
from google import genai
import requests
import os

app = Flask(__name__)

# ----- CONFIG -----
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Member messages API
MEMBER_MESSAGES_API = "https://november7-730026606190.europe-west1.run.app/messages/"

# ----- HELPER: Fetch messages from public API -----
def fetch_member_messages(limit=500):
    messages = []
    skip = 0
    while True:
        resp = requests.get(MEMBER_MESSAGES_API, params={"skip": skip, "limit": limit})
        if resp.status_code != 200:
            break
        data = resp.json()
        items = data.get("items", [])
        if not items:
            break
        messages.extend(items)
        skip += limit
    return messages

# ----- HELPER: Ask Gemini -----
def ask_gemini(question, context):
    """
    Uses Gemini API to answer question based on context
    """
    prompt = f"Answer the following question based on the member messages:\n\n{context}\n\nQuestion: {question}"
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"

# ----- WEB INTERFACE -----
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Ask Gemini AI</title>
</head>
<body>
    <h1>Ask Gemini AI</h1>
    <form method="POST" action="/ask">
        <input type="text" name="question" placeholder="Enter your question" style="width:300px">
        <button type="submit">Ask</button>
    </form>
    {% if answer %}
    <h3>Answer:</h3>
    <p>{{ answer }}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question")
    if not question:
        return render_template_string(HTML_TEMPLATE, answer="Please enter a question!")

    # Fetch messages and build context
    messages = fetch_member_messages(limit=100)
    context = "\n".join([f"{msg['user_name']}: {msg['message']}" for msg in messages])

    # Ask Gemini
    answer = ask_gemini(question, context)
    return render_template_string(HTML_TEMPLATE, answer=answer)

# Optional: API endpoint for JSON requests
@app.route("/api/ask", methods=["POST"])
def api_ask():
    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"error": "Please provide a question in JSON body"}), 400
    
    question = data["question"]
    messages = fetch_member_messages(limit=100)
    context = "\n".join([f"{msg['user_name']}: {msg['message']}" for msg in messages])
    answer = ask_gemini(question, context)
    return jsonify({"answer": answer})

# ----- RUN -----
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
