from flask import Flask, request, jsonify
from flask_cors import CORS
import cohere
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re
import requests
from db import log_result  


load_dotenv()

app = Flask(__name__)
CORS(app)

cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))

def search_fact_check_api(query):
    try:
        api_key = os.getenv("GOOGLE_FACT_CHECK_API_KEY")
        if not api_key:
            print("Missing GOOGLE_FACT_CHECK_API_KEY")
            return None

        url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={requests.utils.quote(query)}&key={api_key}"
        res = requests.get(url, timeout=5)

        if "application/json" not in res.headers.get("Content-Type", ""):
            print("Fact Check API returned non-JSON response")
            return None

        data = res.json()
        print("Fact Check API raw response:", data)

        if "claims" in data:
            for claim in data["claims"]:
                if "claimReview" in claim:
                    return claim["claimReview"][0]["url"]
    except Exception as e:
        print("Fact Check API failed:", e)

    return None

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    ad_text = data.get("text", "").strip()

    if not ad_text:
        return jsonify({"status": "error", "message": "No ad text provided"}), 400

    prompt = f"""
You are a truthful advertising analyst. Classify the following ad claim as:

"Safe" if it is standard, realistic marketing  
"Exaggerated" if it makes big claims without facts  
"Misleading" if it's false, deceptive, or untrue  

Ad: "{ad_text}"  
Respond with only one word: Safe, Exaggerated, or Misleading.
"""

    try:
        response = cohere_client.chat(
            message=prompt,
            model="command-r",
            temperature=0
        )

        output_text = response.text.strip().lower()
        print("Cohere response:", output_text)

        if "misleading" in output_text:
            verdict = "Misleading"
            trust_score = 30
        elif "exaggerated" in output_text:
            verdict = "Exaggerated"
            trust_score = 60
        elif "safe" in output_text:
            verdict = "Safe"
            trust_score = 90
        else:
            verdict = "Unknown"
            trust_score = 50

        reference_url = search_fact_check_api(ad_text)

        log_result(ad_text, verdict, trust_score, reference_url)

        return jsonify({
            "status": "success",
            "verdict": verdict,
            "trust_score": trust_score,
            "reference_url": reference_url or "Not found"
        })

    except Exception as e:
        print("Exception:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

