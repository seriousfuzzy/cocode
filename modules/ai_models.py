# ai_models.py

from langchain_groq import ChatGroq

def init_chat_model():
    # Initialize and return the ChatGroq model
    # You can set up any necessary environment variables or configuration here
    model = ChatGroq(model_name="llama3-70b-8192", temperature=0.2)
    return model

def analyze_resumes(model, resumes_text, job_description):
    # Perform analysis using the model on provided resumes and job description
    prompt = f"""
    Job Description: {job_description}

    Analyze the following resumes based on their relevance to the job description. 
    For each resume, provide:
    1. A relevance score (0-100)
    2. Key skills that match the job description
    3. Relevant experience
    4. A brief explanation (1-2 sentences) of why they are a good fit

    Resumes:
    {resumes_text}

    Format your response as a numbered list, sorted by relevance score (highest to lowest):
    1. [Filename] - Relevance Score: [Score]
       Skills: [Key skills]
       Experience: [Relevant experience]
       Explanation: [Brief explanation]
    2. ...
    """
    
    response = model.invoke(prompt)
    return response.content

def generate_questions(model, resume, job_description):
    prompt = f"""
    Based on the following resume and job description, generate 6 tailored questions to ask the candidate during an interview.

    The first 3 questions MUST:
    - Be based solely on the candidate's resume/CV
    - Be highly relevant to the specific requirements and skills mentioned in the job description
    - Relate directly to the candidate's experience, projects, and skills as described in their resume

    The next 3 questions MUST:
    - Be based directly on the job description
    - Test the candidate's critical thinking abilities in the context of the job role
    - Evaluate the candidate's practical skillset as it applies to the job requirements

    ALL questions should:
    - Be straightforward and concise
    - Not include any explanations or additional context

    Resume:
    {resume}

    Job Description:
    {job_description}

    Format your response as a numbered list of 6 questions, and nothing else:
    1. [CV-based Question 1]
    2. [CV-based Question 2]
    3. [CV-based Question 3]
    4. [Job Description-based Question 1]
    5. [Job Description-based Question 2]
    6. [Job Description-based Question 3]
    """

    response = model.invoke(prompt)
    return response.content