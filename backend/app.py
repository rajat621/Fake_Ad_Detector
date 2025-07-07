# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import cohere
import os
from dotenv import load_dotenv
import requests
# Assuming db.py exists in the same directory and contains the log_result function
from db import log_result 

# Load environment variables from a .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for all routes
# This is important for allowing a frontend application on a different domain
# to make requests to this API.
CORS(app)

# Initialize the Cohere client using the API key from environment variables
# Ensure COHERE_API_KEY is set in your .env file or environment.
cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))

def search_fact_check_api(query):
    """
    Searches the Google Fact Check Tools API for claims related to the given query.

    Args:
        query (str): The text query (e.g., an ad claim) to search for.

    Returns:
        str or None: The URL of a relevant fact-check article if found, otherwise None.
    """
    try:
        # Retrieve the Google Fact Check API key from environment variables.
        # Ensure GOOGLE_FACT_CHECK_API_KEY is set.
        api_key = os.getenv("GOOGLE_FACT_CHECK_API_KEY")
        if not api_key:
            print("Missing GOOGLE_FACT_CHECK_API_KEY environment variable.")
            return None

        # Construct the API URL. requests.utils.quote is used to safely encode the query.
        url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={requests.utils.quote(query)}&key={api_key}"
        
        # Make a GET request to the Fact Check API with a 5-second timeout.
        res = requests.get(url, timeout=5)

        # Check if the response content type is JSON.
        if "application/json" not in res.headers.get("Content-Type", ""):
            print("Fact Check API returned non-JSON response.")
            return None

        # Parse the JSON response.
        data = res.json()
        print("Fact Check API raw response:", data) # For debugging purposes

        # Check if 'claims' exist in the response and iterate through them.
        if "claims" in data:
            for claim in data["claims"]:
                # If a claim has 'claimReview', return the URL of the first review.
                if "claimReview" in claim and len(claim["claimReview"]) > 0:
                    return claim["claimReview"][0]["url"]
    except requests.exceptions.RequestException as req_e:
        print(f"Fact Check API request failed: {req_e}")
    except Exception as e:
        print(f"An unexpected error occurred with Fact Check API: {e}")

    return None

@app.route("/analyze", methods=["POST"])
def analyze():
    """
    API endpoint to analyze an ad claim using Cohere and Google Fact Check API.

    Expects a JSON payload with a 'text' field containing the ad claim.
    Example request body: {"text": "This product will make you fly!"}

    Returns:
        JSON response with analysis verdict, trust score, and a reference URL.
    """
    # Get JSON data from the request body.
    data = request.get_json()
    # Extract and strip whitespace from the 'text' field.
    ad_text = data.get("text", "").strip()

    # Validate if ad text is provided.
    if not ad_text:
        return jsonify({"status": "error", "message": "No ad text provided"}), 400

    # Define the prompt for the Cohere model.
    # The prompt instructs the model to classify the ad claim into "Safe", "Exaggerated", or "Misleading".
    # It also specifies the desired single-word response format.
    prompt = f"""
You are a truthful advertising analyst. Classify the following ad claim as:

"Safe" if it is standard, realistic marketing
"Exaggerated" if it makes big claims without facts
"Misleading" if it's false, deceptive, or untrue

Ad: "{ad_text}"
Respond with only one word: Safe, Exaggerated, or Misleading.
"""

    try:
        # Call the Cohere Chat API to get the classification.
        # Using 'command-r' model and 'temperature=0' for deterministic classification.
        response = cohere_client.chat(
            message=prompt,
            model="command-r",
            temperature=0
        )

        # Process the Cohere model's response.
        output_text = response.text.strip().lower()
        print("Cohere response:", output_text) # For debugging purposes

        # Determine the verdict and trust score based on the Cohere output.
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
            # Fallback for unexpected Cohere responses.
            verdict = "Unknown"
            trust_score = 50

        # Attempt to find a fact-check reference URL.
        reference_url = search_fact_check_api(ad_text)

        # Log the analysis result using the function from db.py.
        # This function needs to be implemented in db.py to store the data.
        log_result(ad_text, verdict, trust_score, reference_url)

        # Return the analysis results as a JSON response.
        return jsonify({
            "status": "success",
            "verdict": verdict,
            "trust_score": trust_score,
            "reference_url": reference_url or "Not found" # Provide "Not found" if no URL is returned
        })

    except cohere.CohereError as cohere_e:
        print(f"Cohere API error: {cohere_e}")
        return jsonify({"status": "error", "message": f"Cohere API error: {cohere_e}"}), 500
    except Exception as e:
        # Catch any other unexpected exceptions and return an error.
        print(f"An unexpected exception occurred during analysis: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# This block ensures the Flask app runs only when the script is executed directly.
if __name__ == "__main__":
    # Run the Flask application.
    # host="0.0.0.0" makes the server accessible externally (important for deployment).
    # port is taken from the 'PORT' environment variable, defaulting to 5000 if not set.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
