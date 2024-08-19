import streamlit as st
from datetime import datetime
from modules.ai_models import init_chat_model, analyze_resumes, generate_questions
from modules.database import init_db, add_candidate, get_latest_candidates
from modules.resume import process_pdf, create_vector_store
from modules.tempfile_util import clean_temp_files
import os
import io

# Function to load environment variables


def load_env():
    try:
        from dotenv import load_dotenv
        load_dotenv('.env')
    except ImportError:
        st.warning(
            "Python-dotenv library is not installed. Install it using 'pip install python-dotenv'.")

    if 'GROQ_API_KEY' not in os.environ:
        st.error(
            "GROQ_API_KEY is not set in the environment variables. Please set it and try again.")
        st.stop()


# Initialize database
conn = init_db()

# Initialize AI model and embeddings
load_env()  # Load environment variables including GROQ_API_KEY

chat_model = init_chat_model()


def dashboard():
    st.title("Dashboard")
    st.write("Welcome to the AI-Powered Resume Ranker for HR")
    # Add any dashboard-specific content here


def resume_ranker():
    st.title("Resume Ranker")
    uploaded_files = st.file_uploader(
        "Upload resumes (PDF files)", type="pdf", accept_multiple_files=True)
    job_description = st.text_area(
        "Enter the job description or key requirements:")

    if uploaded_files and job_description:
        st.write(f"Processing {len(uploaded_files)} resumes...")

        all_documents = []
        for uploaded_file in uploaded_files:
            pages = process_pdf(uploaded_file)
            all_documents.extend(pages)

        vector_store = create_vector_store(all_documents)

        similar_docs = vector_store.similarity_search(job_description, k=5)
        resumes_text = "\n\n".join(
            [f"{doc.metadata['source']}: {doc.page_content}" for doc in similar_docs])

        analysis = analyze_resumes(chat_model, resumes_text, job_description)

        st.subheader("Top 5 Ranked Candidates")
        st.write(analysis)

    else:
        st.write(
            "Please upload PDF resumes and enter a job description to start analyzing.")

    if st.button("Clear All Uploads"):
        clean_temp_files()


def questions_for_candidate():
    st.title("Questions for the Candidate")

    # Job Description input
    job_desc_method = st.radio("Job Description Input Method", [
                               "Enter Text", "Upload File"])

    if job_desc_method == "Enter Text":
        job_description = st.text_area("Enter the job description:")
    else:
        job_desc_file = st.file_uploader(
            "Upload Job Description", type=["pdf", "txt"])
        if job_desc_file:
            if job_desc_file.type == "application/pdf":
                job_description = "\n".join(
                    [doc.page_content for doc in process_pdf(job_desc_file)])
            else:  # Assume it's a text file
                job_description = job_desc_file.getvalue().decode("utf-8")
        else:
            job_description = ""

    # Candidate Resume upload
    resume_file = st.file_uploader(
        "Upload Candidate's Resume (PDF)", type="pdf")

    if resume_file:
        candidate_resume = "\n".join(
            [doc.page_content for doc in process_pdf(resume_file)])
    else:
        candidate_resume = ""

    if st.button("Generate Questions"):
        if job_description and candidate_resume:
            questions = generate_questions(
                chat_model, candidate_resume, job_description)
            st.subheader("Interview Questions")
            st.write(questions)
        else:
            st.error(
                "Please provide both the job description and candidate's resume.")


def add_candidate():
    st.title("Add Candidate")
    candidate_name = st.text_input("Candidate Name")
    candidate_email = st.text_input("Candidate Email")
    job_applied = st.text_input("Job Applied For")
    relevance_score = st.number_input(
        "Relevance Score (0-100)", min_value=0, max_value=100)
    resume_filename = st.text_input("Resume Filename")

    if st.button("Add Candidate"):
        if candidate_name and candidate_email and job_applied and resume_filename:
            add_candidate(conn, candidate_name, candidate_email,
                          resume_filename, job_applied, relevance_score, datetime.now())
            st.success("Candidate added to database successfully!")
        else:
            st.error("Please fill in all fields.")

    st.subheader("Recent Candidates")
    candidates = get_latest_candidates(conn, limit=10)
    for candidate in candidates:
        st.write(
            f"Name: {candidate[1]}, Email: {candidate[2]}, Job Applied: {candidate[4]}, Relevance Score: {candidate[5]}")


def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", [
                                 "Dashboard", "Resume Ranker", "Questions for the Candidate", "Add Candidate"])

    if selection == "Dashboard":
        dashboard()
    elif selection == "Resume Ranker":
        resume_ranker()
    elif selection == "Questions for the Candidate":
        questions_for_candidate()
    elif selection == "Add Candidate":
        add_candidate()


if __name__ == "__main__":
    main()

# Close the database connection when the app is done
conn.close()
