import google.generativeai as genai
import json 

API_KEY = 'AIzaSyBisQCOGKjW2RU34Da6BJ2cGV9vtAkiKCI'
genai.configure(api_key=API_KEY)


# For safety settings, if needed, though default should be okay for this
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}
# ... (the rest of your script, including the model instantiation)


generator_config = {
    "temperature": 0.7, # Controls randomness. Lower for more factual.
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

job_posting = """
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

sample_resume_good_match = """
Jane Doe
jane.doe@email.com | (555) 123-4567 | linkedin.com/in/janedoe

Summary
Versatile Software Engineer with 5+ years of experience with full stack development and expertise in Python and Java.  I have proven experience in employing the entire SDLC process through concept to deploy.  I have utilized development best practices, an agile mentality and CI/CD pipeline for best results.

Experience
Senior Software Engineer | Tech Solutions Inc. | 2019 – Present
- Lead development and implementation of key features and functionality for a flagship product using Python, Django and PostgreSQL.
- Developed RESTful APIs for microservices.
- Participated in Agile sprints, code reviews and architectural discussions on a regular basis.
- Provided mentorship to junior engineers on software development best practices and improved the overall quality the team’s code.
- Used Jenkins to implement CI/CD pipelines improving deployment times by 30%.
- Developed and implemented using AWS services including EC2, S3 and RDS.

Software Engineer | Web Wizards LLC | 2017 – 2019
- Responsible for development and maintenance of a web-based application using Java, Spring Boot, MySQL, etc.
- Involved in the SDLC process from concept to implementation.
- I worked closely with cross-functional teams to define and design new features. 

Education
BSc in Computer Science | State University | 2017

Skills
Programming Language Skills: Python, Java, JavaScript, C++ (basic skills)
Frameworks: Django, Spring Boot, React
Database Skills: PostgreSQL, MySQL, MongoDB (basic)
Tools: Git, Docker, Jenkins, Jira
Cloud: AWS (EC2, S3, RDS)
Methodologies: Agile, Scrum
"""

sample_resume_poor_match = """
John Smith
john.smith@email.com | (555) 987-6543

Objective
Seeking challenging marketing role where I can demonstrate creative and analytical skills.

Experience
Marketing Intern | Creative Ads Co. | Summer 2023
- Assisted with social media campaigns.
- Conducted market research.

Education
BA in Marketing | City College | 2024

Skills
Social Media Marketing, Content Creation, Market Research, Microsoft Office
"""

resume_screening_prompt = f"""
You are an expert HR AI assistant focused on resume screening for Software Engineer positions.
Your job is to examine the provided resume against the given job description.

Job Description:
---
{job_posting}
---

Resume:
---
{{resume_text}}
---

Submit your response with the following:
1.  Overall match score (0-100%): A percentage score that tells how well the resume matches the job description.
2.  Matching skills: A list of the key skills from the job description that are found in the resume.
3.  Missing skills: A list of the key skills from the job description that are NOT PRESENT or lacking from the resume.
4.  Experience summary: A brief summary of the candidate's experience as it relates to the job description.
5.  Red flags (if any): An reference for anything questionable or a clear mismatch. If none, state 'No red flags'
6.  Suggested Fit: (Good Fit / Potential Fit / Poor Fit)

Please format your output in a way that is easy to read.
"""

def screen_resume(resume_content):
    prompt_parts = [resume_screening_prompt.format(resume_text=resume_content)]
    print("--- Sending request to Gemini API for Resume Screening ---")
    try:
        response = model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        return f"Error: {e}\nDetails: {getattr(e, 'message', str(e))}"


print("--- Screening Good Match Resume ---")
good_match_analysis = screen_resume(sample_resume_good_match)
print(good_match_analysis)

print("\n\n--- Screening Poor Match Resume ---")
poor_match_analysis = screen_resume(sample_resume_poor_match)
print(poor_match_analysis)