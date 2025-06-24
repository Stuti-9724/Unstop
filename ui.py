
import streamlit as st
import requests

st.set_page_config(page_title="HR AI Vibes", page_icon="🤖", layout="centered")

st.title("🤖 HR AI Toolkit")
st.markdown("Analyze resumes and employee feedback — powered by Gemini 💫")

st.sidebar.title("🛠 Tools")
tool = st.sidebar.radio("Choose a tool:", ["Resume Screener", "Sentiment Analyzer"])

# Set your local Flask API URL
API_URL = "http://127.0.0.1:5000"

if tool == "Resume Screener":
    st.header("📄 Resume Screener")
    resume = st.text_area("Paste Resume Text", height=200)
    jd = st.text_area("Optional: Paste Job Description", height=150)

    if st.button("🧠 Analyze Resume"):
        if not resume:
            st.warning("Please paste a resume to analyze.")
        else:
            with st.spinner("Contacting HR AI model..."):
                payload = {"resume_text": resume}
                if jd:
                    payload["job_description"] = jd
                response = requests.post(f"{API_URL}/screen_resume", json=payload)
                result = response.json()

                if "resume_analysis" in result:
                    st.success("✅ Analysis Complete!")
                    st.markdown(result["resume_analysis"])
                else:
                    st.error(result.get("error", "Something went wrong."))

elif tool == "Sentiment Analyzer":
    st.header("💬 Sentiment Analyzer")
    feedback = st.text_area("Paste Employee Feedback", height=150)

    if st.button("🔍 Analyze Sentiment"):
        if not feedback:
            st.warning("Please paste some feedback.")
        else:
            with st.spinner("Contacting HR AI model..."):
                response = requests.post(f"{API_URL}/analyze_sentiment", json={"feedback_text": feedback})
                result = response.json()

                if "sentiment_analysis" in result:
                    st.success("✅ Analysis Complete!")
                    st.markdown(result["sentiment_analysis"])
                else:
                    st.error(result.get("error", "Something went wrong."))
