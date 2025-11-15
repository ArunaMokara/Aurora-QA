# Ask Gemini AI – Question Answering System

## Project Overview
This is a **question-answering web application** that allows users to ask questions based on publicly available member messages. The system uses **Google’s Gemini API (free tier)** to generate context-aware answers.

The project is deployed on **Render.com free tier**, making it accessible via a public URL without any paid infrastructure.

---

## Features

- Web interface for asking questions (`/ask`).
- Dynamically fetches messages from a public API to build context.
- Uses **Google Gemini API** (free tier) for high-quality natural language answers.
- Fully deployed on **Render free tier** — no payment required.

---

## Live Demo

Access the deployed app here:  

https://aurora-qa-eqhl.onrender.com/

- Web form: `/ask`

## Project Structure
.
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── Procfile            # For Render deployment
├── README.md           # Project documentation

## Setup & Running Locally
### 1. Clone the repository
git clone <your-repo-url>
cd <repo-folder>

### 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows

### 3. Install dependencies
pip install -r requirements.txt

### 4. Set environment variable
export GEMINI_API_KEY="your_free_gemini_api_key"   # Linux / Mac
set GEMINI_API_KEY="your_free_gemini_api_key"      # Windows

### 5. Run the app locally
python app.py

## Deployment (Render Free Tier)
1.Connect your GitHub repo to Render.
2.Add GEMINI_API_KEY as an environment variable in Render.
3.Create a Procfile: web: gunicorn app:app

Render will handle deployment; the app is available at a public URL.
Note: Free-tier services may go to sleep after inactivity, but the link stays valid.

## Bonus 1: Design Notes – Alternative Approaches

While building this system, several approaches were considered:
### Local LLM (LLaMA, MPT)
No API needed, but requires GPU and more setup.

### Vector DB + Embeddings
Store messages as embeddings for semantic search.

### Efficient for large datasets but adds extra infrastructure.

### Rule-based / Keyword Matching
Fast, no ML needed, but cannot understand complex queries.

### Hybrid Approach
Combine semantic search + LLM for precise answers.
More complex but reduces API calls.

### Different LLM APIs
Alternatives: OpenAI GPT, Cohere, Anthropic.
Chosen: Google Gemini (free tier, good quality, minimal setup).

## Conclusion:
The current approach was chosen for simplicity, free-tier availability, and ease of deployment.
