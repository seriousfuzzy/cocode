<p align='center'>
  <img src='public/easy-hiring.png' alt='logo' width='200px'/>
</p>

# AI-Powered Resume Ranker for HR

This Streamlit application automates the process of ranking job candidates based on their resumes against a job description. It utilizes AI models for resume analysis and question generation for interviews.

## Features

- **Upload Resumes:** Upload multiple PDF resumes for analysis.
- **Job Description Input:** Enter the job description or key requirements.
- **Resume Analysis:** Rank resumes based on relevance to the job description.
- **Interview Questions:** Generate tailored interview questions for top-ranked candidates.
- **Database Integration:** Add candidates to a SQLite database and view the latest candidates.

## Installation

```bash
git clone https://github.com/Sinarc-co/easy-hiring.git
cd easy-hiring
pip install -r requirements.txt
```
Create a `.env` file with your `GROQ_API_KEY`:
```bash
GROQ_API_KEY=your_api_key_here
```

## Usage
```bash
streamlit run main.py
```
Upload PDF resumes and enter the job description to start analyzing.

## Folder Structure
```
├── main.py            # Main application script
├── modules/
│   ├── ai_models.py   # AI model initialization and resume analysis
│   ├── database.py    # SQLite database initialization and operations
│   ├── resume.py      # PDF processing and vector store creation
│   └── tempfile_util.py  # Temporary file handling
└── candidates.db      # SQLite database file
```

## Screenshots

### Resume Score
<p align='center'>
  <img src='screenshots/resume_score.png' alt='Resume Score'/>
</p>

### Interview Questions
<p align='center'>
  <img src='screenshots/interview_qs.png' alt='Interview Qs'/>
</p>

### Adding Candidate to DB
<p align='center'>
  <img src='screenshots/db.png' alt='DB'/>
</p>

## Contributing
Contributions are welcome! Please fork the repository and create a pull request for any bug fixes or improvements.

Experience seamless resume analysis or refine your own to enhance your career journey!