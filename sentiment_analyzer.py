import google.generativeai as genai

SENTIMENT_GUIDE = """
You are an efficient HR AI assistant, experienced in understanding employee sentiment.
Your goal is to analyze the provided employee feedback text.

Employee Feedback:
---
{feedback_text}
---

Based on the feedback, please provide:
1.  Sentiment: Classify as (Positive / Negative / Neutral).
2.  Key Points: What are the main topics or issues raised?
3.  Attrition Risk: (High / Medium / Low / Not Applicable).especially if the sentiment is negative or expresses dissatisfaction.
4.  Actionable Suggestions: If issues are there or attrition risk is high, offer 1-2 short, practical strategies to resolve them. If the feedback is positive, suggest how to maintain that sentiment.
"""

def analyze_employee_sentiment(llm_model, employee_feedback_text):
    """
    Uses a given LLM model to analyze employee feedback text.

    Args:
        llm_model: An initialized google.generativeai.GenerativeModel instance.
        employee_feedback_text (str): The text of the employee's feedback.

    Returns:
        str: The LLM's sentiment analysis, or an error message.
    """
    prompt_llm = SENTIMENT_GUIDE.format(feedback_text=employee_feedback_text)
    prompt_parts = [prompt_llm]

    print("--- [Sentiment Analyzer] Contacting Gemini for analysis... ---")
    try:
        response = llm_model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        import traceback
        print(f"--- [Sentiment Analyzer] ERROR during API call: {traceback.format_exc()} ---")
        return f"An error occurred while analyzing sentiment: {str(e)}"

# This section is for directly testing the sentiment analyzer module.
if __name__ == '__main__':
    print("--- Running sentiment_analyzer.py in standalone test mode ---")

    TEST_API_KEY = 'AIzaSyBisQCOGKjW2RU34Da6BJ2cGV9vtAkiKCI'
    if TEST_API_KEY == 'YOUR_ACTUAL_API_KEY_FOR_TESTING':
        print("WARNING: Please replace 'YOUR_ACTUAL_API_KEY_FOR_TESTING' with your real API key to test.")
        exit()

    genai.configure(api_key=TEST_API_KEY)

    test_gen_config = {"temperature": 0.7, "max_output_tokens": 1024}
    test_safety = [
        {"category": c, "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
        for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH",
                  "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]
    ]

    try:
        standalone_test_model = genai.GenerativeModel(
            model_name="models/gemini-1.5-flash-latest",
            generation_config=test_gen_config,
            safety_settings=test_safety
        )
        print("Test model initialized.")

        # Sample feedback for testing
        positive_msg = "I'm really enjoying the new project challenges and my team is incredibly supportive!"
        negative_note = "The workload has become unmanageable, and I feel completely burnt out. I'm considering other options."
        neutral = "The recent software update is okay, but more comprehensive training documentation would be beneficial."

        print("\n--- Analyzing Positive Feedback ---")
        print(analyze_employee_sentiment(standalone_test_model, positive_msg))

        print("\n--- Analyzing Negative Feedback (Potential Attrition) ---")
        print(analyze_employee_sentiment(standalone_test_model, negative_note))

        print("\n--- Analyzing Neutral/Constructive Feedback ---")
        print(analyze_employee_sentiment(standalone_test_model, neutral))

    except Exception as e:
        print(f"An error occurred during standalone testing: {e}")