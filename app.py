import streamlit as st
import fitz
from docx import Document
from ollama import chat
import re

st.title("AI Resume Analyzer")
st.write("Welcome to my AI Resume Analyzer!")
st.write("Upload your resume and get AI-powered feedback.")
st.sidebar.title("📌 Resume Analyzer")
st.sidebar.write("Analyze your resume against a job description.")

st.sidebar.markdown("""
### Features
- 📄 PDF & DOCX Resume
- 🔍 Skill Detection
- 🎯 Job Skill Matching
- 🤖 AI Resume Analysis
- 💡 Improvement Suggestions
""")
st.divider()
##file got uploaded
uploaded_file = st.file_uploader(
    "Choose your resume",
    type=["pdf","docx"]
)

##job description 
job_description = st.text_area(
    "Paste the Job Description",
    height=200
)

if uploaded_file:
    st.success("File uploaded successfully!")
    st.write("File name:", uploaded_file.name)
    st.write("File Size:", uploaded_file.size, "bytes")

    if uploaded_file.name.endswith(".pdf"):

        pdf = fitz.open(
            stream=uploaded_file.read(),
            filetype="pdf"
        )

        resume_text = ""

        for page in pdf:
            resume_text += page.get_text()

    elif uploaded_file.name.endswith(".docx"):

        document = Document(uploaded_file)

        resume_text = ""

        for paragraph in document.paragraphs:
            resume_text += paragraph.text + "\n"

    st.subheader("Extracted Resume Text")
    st.text(resume_text)

    
    ##what skills are there in resume
    skills = [
    "Python",
    "Java",
    "SQL",
    "HTML",
    "CSS",
    "JavaScript",
    "Git",
    "GitHub",
    "MySQL",
    "C++",
    "Django",
    "React",
    "REST APIs",
    "PostgreSQL",
    "Docker",
    "AWS",
    "Generative AI",
    "LLM"]

    skill_aliases = {
    "HTML": ["HTML", "HTML5"],
    "CSS": ["CSS", "CSS3"],
    "React": ["React", "React.js"],
    "LLM": ["LLM", "Large Language Model", "Large Language Models"]
    }
    detected_skills = []

    resume_lower = resume_text.lower()

    for skill in skills:

        if skill in skill_aliases:
            aliases = skill_aliases[skill]
        else:
            aliases = [skill]

        for alias in aliases:
            pattern = r"\b" + re.escape(alias.lower()) + r"\b"

            if re.search(pattern, resume_lower):
                detected_skills.append(skill)
                break

    st.subheader("Detected Skills")

    if detected_skills:
        for skill in detected_skills:
            st.write("✅", skill)
    else:
        st.write("No skills detected.")
##skills matching or missing 
    job_skills = []

    job_lower = job_description.lower()

    for skill in skills:

        if skill in skill_aliases:
            aliases = skill_aliases[skill]
        else:
            aliases = [skill]

        for alias in aliases:
            pattern = r"\b" + re.escape(alias.lower()) + r"\b"

            if re.search(pattern, job_lower):
                job_skills.append(skill)
                break

    st.subheader("Job Required Skills")

    if job_skills:
        for skill in job_skills:
            st.write("🔹", skill)
    else:
        st.write("No skills detected from the job description.")
    # Matching and missing skills
    matching_skills = []
    missing_skills = []

    resume_lower = resume_text.lower()

    for skill in job_skills:

        if skill in skill_aliases:
            aliases = skill_aliases[skill]
        else:
            aliases = [skill]

        skill_found = False

        for alias in aliases:
            pattern = r"\b" + re.escape(alias.lower()) + r"\b"

            if re.search(pattern, resume_lower):
                skill_found = True
                break

        if skill_found:
            matching_skills.append(skill)
        else:
            missing_skills.append(skill)   
##add AI analysis
    st.subheader("🤖 AI Resume Analysis")
    if not job_description:

        st.info("Please paste a Job Description to analyze your resume.")

    elif st.button("🚀 Analyze Resume"):
   
        prompt = f"""
You are a professional resume analyzer.

Analyze the following resume against the job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

VERIFIED RESUME SKILLS:
{detected_skills}

VERIFIED JOB SKILLS:
{job_skills}

VERIFIED MISSING SKILLS:
{missing_skills}

Use the verified skill results as the source of truth.

Rules:
- Do not claim the candidate has a skill that is not in VERIFIED RESUME SKILLS.
- Do not say the resume has experience with a missing skill.
- Do not invent projects, certifications, work experience, or technologies.
- If a skill is missing, clearly identify it as missing.
- Base your suggestions only on information present in the resume and job description.


Give your analysis in these sections:

1. Resume Strengths
2. Missing or Weak Skills
3. Resume Improvement Suggestions
4. Job Match Observations

Keep the explanation simple and practical.
"""

        try:
            with st.spinner("🤖 AI is analyzing your resume..."):
                response = chat(
                    model="llama3.2:3b",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
                st.write(response.message.content)

        except Exception as e:

            st.error("Could not connect to Ollama.")
            st.info(
                "Please make sure Ollama is running and try again."
            )

            st.write("Error:", e)
    
    # Calculate job skill match percentage

    if job_skills:
        match_percentage = (
            len(matching_skills) / len(job_skills)
        ) * 100

        st.subheader("🎯 Job Skill Match")

        st.metric(
            label="Skill Match",
            value=f"{match_percentage:.0f}%"
        )

        st.caption(
            "This percentage is based only on the detected skills "
            "listed in the job description."
        )
    else:
        st.write("Job match percentage cannot be calculated.")
    

    st.subheader("Skills to Improve")

    if missing_skills:
        for skill in missing_skills:
            st.write("⚠️", skill)
    else:
        st.write("No missing skills found.")

