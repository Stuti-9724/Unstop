import google.generativeai as genai
# Was thinking of using a different model
# model = genai.GenerativeModel(model_name="gemini-1.5-pro")


API_KEY = 'AIzaSyBisQCOGKjW2RU34Da6BJ2cGV9vtAkiKCI'
genai.configure(api_key=API_KEY)

generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Testing with a few sample feedback messages
positive_msg = "I love working here! The team is supportive and the projects here are difficult yet fulfilling. My manager is amazing."
negative_note = "I'm feeling exhausted. The workload has been crazy, and I don't see any recognition for the overtime. I'm starting to look for other opportunities."
neutral= "The new softwares are okay, but the onboarding could have been better. More training would be helpful."

# Optimizing and traing using prompt engineering
prompt = """
You are an expert HR AI assistant specialized in employee sentiment analysis.
Your task is to analyze the provided employee feedback.

Employee Feedback:
---
{feedback_text}
---

Please provide the following:
1.  Tone of the feedback: (Positive / Negative / Neutral)
2.  Key Reasons: Identify the main topics mentioned in the feedback.
3.  Attrition Risk (if valid): (High / Medium / Low / Not relevant). Judge this mainly if sentiment is negative or shows dissatisfaction.
4.  Suggest what can be done (if applicable, especially for negative/neutral feedback or attrition risk): Suggest 1-2 brief, paln of action to deal with the feedback. If positive, suggest how to maintain it.
"""

def analyze(feedback_content):
    parts = [prompt.format(feedback_text=feedback_content)]
    print("--- Sending request to Gemini for Sentiment Analysis ---")
    try:
        response = model.generate_content(parts)
        return response.text
    except Exception as e:
        return f"Error: {e}\nDetails: {getattr(e, 'message', str(e))}"

print("--- Analyzing Positive Feedback ---")
positive_analysis = analyze(positive_msg)
print(positive_analysis)

print("\n\n--- Analyzing Negative Feedback (Attrition Risk) ---")
negative_analysis = analyze(negative_note)
print(negative_analysis)

print("\n\n--- Analyzing Neutral/Constructive Feedback ---")
neutral_analysis = analyze(neutral)
print(neutral_analysis)