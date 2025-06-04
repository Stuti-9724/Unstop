# This Flask app is an API gateway for our HR AI tools.
from flask import Flask, request, jsonify
import google.generativeai as genai
import os 

from resume_screener import screen_resume_with_llm, DEFAULT_JOB_DESCRIPTION
from sentiment_analyzer import analyze_employee_sentiment

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') 
if not GEMINI_API_KEY:
    GEMINI_API_KEY = 'AIzaSyBisQCOGKjW2RU34Da6BJ2cGV9vtAkiKCI' 
    if GEMINI_API_KEY == 'YOUR_FALLBACK_API_KEY_HERE':
        print("WARNING: GEMINI_API_KEY not found in environment. Using fallback. "
              "Please set the GEMINI_API_KEY environment variable or update the fallback.")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    print("Google Generative AI configured successfully.")
except Exception as e:
    print(f"ERROR: Failed to configure Google Generative AI: {e}")

LLM_MODEL_NAME = "models/gemini-1.5-flash-latest" 

llm_generation_config = {
    "temperature": 0.7,
    "top_p": 1.0,
    "top_k": 1,   
    "max_output_tokens": 2048, 
}

llm_safety_settings = [
    {"category": c, "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH",
              "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]
]

hr_ai_model = None
try:
    hr_ai_model = genai.GenerativeModel(
        model_name=LLM_MODEL_NAME,
        generation_config=llm_generation_config,
        safety_settings=llm_safety_settings
    )
    print(f"Successfully initialized LLM: {LLM_MODEL_NAME}")
except Exception as e:
    print(f"CRITICAL ERROR: Could not initialize the LLM ({LLM_MODEL_NAME}): {e}")
    print("The application API endpoints will not function correctly.")
    
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return jsonify({
        "message": "HR AI Tools API is running!",
        "endpoints": {
            "/screen_resume": "POST with {'resume_text': str, 'job_description': str (optional)}",
            "/analyze_sentiment": "POST with {'feedback_text': str}"
        }
    })

@flask_app.route('/screen_resume', methods=['POST'])
def api_screen_resume():
    if not hr_ai_model:
        return jsonify({"error": "AI model is not available. Please check server logs."}), 503

    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "Invalid JSON payload."}), 400

        resume_text = json_data.get('resume_text')
        job_description_text = json_data.get('job_description', DEFAULT_JOB_DESCRIPTION)

        if not resume_text:
            return jsonify({"error": "Missing 'resume_text' in the request."}), 400
        if not job_description_text: 
            return jsonify({"error": "Missing 'job_description' in the request."}), 400

        print(f"Received resume screening request for resume: {resume_text[:50]}...") # Log snippet
        analysis = screen_resume_with_llm(hr_ai_model, resume_text, job_description_text)

        if "An error occurred while screening the resume:" in analysis:
            return jsonify({"error": "Resume screening failed.", "details": analysis}), 500
        return jsonify({"resume_analysis": analysis})

    except Exception as e:
        # Catch-all for unexpected errors during request processing
        print(f"Error in /screen_resume endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "An unexpected server error occurred."}), 500

@flask_app.route('/analyze_sentiment', methods=['POST'])
def api_analyze_sentiment():
    if not hr_ai_model:
        return jsonify({"error": "AI model is not available. Please check server logs."}), 503

    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "Invalid JSON payload."}), 400

        feedback_text = json_data.get('feedback_text')

        if not feedback_text:
            return jsonify({"error": "Missing 'feedback_text' in the request."}), 400

        print(f"Received sentiment analysis request for feedback: {feedback_text[:50]}...") # Log snippet
        analysis = analyze_employee_sentiment(hr_ai_model, feedback_text)

        if "An error occurred while analyzing sentiment:" in analysis:
            return jsonify({"error": "Sentiment analysis failed.", "details": analysis}), 500
        return jsonify({"sentiment_analysis": analysis})

    except Exception as e:
        print(f"Error in /analyze_sentiment endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "An unexpected server error occurred."}), 500

if __name__ == '__main__':
    if not hr_ai_model:
        print("Flask app cannot start properly as the AI model failed to initialize.")
        # exit(1)
    else:
        print("Starting HR AI Tools Flask API...")
        flask_app.run(host='0.0.0.0', port=5000, debug=True)