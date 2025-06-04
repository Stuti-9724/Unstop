import google.generativeai as genai

DEFAULT_JD = """
software engineer
We are finding a qualified Software Engineer to design, develop, and maintain software solutions.
Responsibilities:
- Create high-quality software design and architecture.
- Identify and execute tasks throughout the software development life cycle.
- Develop tools and applications by producing clean, efficient code.
- Automate tasks through appropriate tools and scripts.
- Review and debug code.
- Perform validation and verification testing.
- Collaborate with internal teams and vendors to fix and improve products.
Required skills:
- Proven work experience as a Software Engineer, or similar role.
- Experience working in the Software Development Life Cycle (SDLC).
- Proficiency in Python, Java, or C++.
- Experience working with databases, SQL, or NoSQL.
- Experience with Agile methodologies.
- Excellent problem-solving skills.
- A BSc degree in Computer Science, Engineering or in a relevant field.
Desirable skills:
- Experience with cloud platforms (e.g., AWS, Azure, GCP).
- Knowledge of CI/CD pipelines.
"""

PROMPT = f"""
You are an expert HR AI assistant focused on resume screening for Software Engineer positions.
Your job is to examine the provided resume against the given job description.

Job Description:
---
{{job_description}}
---

Resume:
---
{{resume_text}}
---

Please provide the following, formatted clearly:
1.  Overall Match Score (0-100%): Your assessment of how well the resume aligns with the job description.
2.  Matching Skills: Key skills from the job description that are evident in the resume.
3.  Missing Skills: Important skills from the job description that appear to be absent from the resume.
4.  Experience Summary: A concise overview of the candidate's relevant experience.
5.  Red Flags (if any): Any significant concerns or clear mismatches. If none, please state "No notable red flags."
6.  Suggested Fit: Categorize as (Good Fit / Potential Fit / Poor Fit).
"""

def screen_resume_with_llm(llm_model, candidate_resume_text, job_requirements_text):
    """
    Leverages a given LLM model to screen a resume against job requirements.

    Args:
        llm_model: An initialized google.generativeai.GenerativeModel instance.
        candidate_resume_text (str): The text content of the candidate's resume.
        job_requirements_text (str): The text content of the job description.

    Returns:
        str: The LLM's analysis of the resume, or an error message.
    """
    full = PROMPT.format(
        job_description=job_requirements_text,
        resume_text=candidate_resume_text
    )
    parts = [full]

    print("--- [Resume Screener] Contacting Gemini for analysis... ---")
    try:
        response = llm_model.generate_content(parts)
        return response.text
    except Exception as e:
        import traceback
        print(f"--- [Resume Screener] ERROR during API call: {traceback.format_exc()} ---")
        return f"An error occurred while screening the resume: {str(e)}"

if __name__ == '__main__':
    print("--- Running resume_screener.py in standalone test mode ---")

    TEST_API_KEY = 'AIzaSyBisQCOGKjW2RU34Da6BJ2cGV9vtAkiKCI'
    if TEST_API_KEY == 'YOUR_ACTUAL_API_KEY_FOR_TESTING':
        print("WARNING: Please replace 'YOUR_ACTUAL_API_KEY_FOR_TESTING' with your real API key to test.")
        exit()

    genai.configure(api_key=TEST_API_KEY)


    test_gen_config = {"temperature": 0.7, "max_output_tokens": 2048}
    test_safety = [
        {"category": c, "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
        for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH",
                  "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]
    ]

    try:
        test_model = genai.GenerativeModel(
            model_name="models/gemini-1.5-flash-latest", 
            generation_config=test_gen_config,
            safety_settings=test_safety
        )
        print("Test model initialized.")

        # Sample data for testing
        good = """
        Jane Doe - jane.doe@email.com
        Highly skilled Python and Java developer with 5 years experience in full-stack development,
        agile methodologies, and CI/CD pipelines. BSc Computer Science.
        """
        poor = """
        John Smith - john.smith@email.com
        Looking for a marketing role. Experience with social media.
        """

        print("\n--- Testing with a 'Good Fit' Resume ---")
        analysis_good = screen_resume_with_llm(test_model, good, DEFAULT_JD)
        print(analysis_good)

        print("\n--- Testing with a 'Poor Fit' Resume ---")
        analysis_poor = screen_resume_with_llm(test_model, poor, DEFAULT_JD)
        print(analysis_poor)

    except Exception as e:
        print(f"An error occurred during standalone testing: {e}")