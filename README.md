# AI Resume ATS System 🚀

An AI-powered Application Tracking System (ATS) designed to analyze resumes, calculate match scores against job descriptions, and provide actionable feedback to job seekers. Built using Python, HTML, and CSS.

## 🌟 Features
- **ATS Score Generation**: Evaluates resumes against specific job descriptions.
- **Keyword Optimization**: Identifies missing technical and soft skills.
- **Detailed Analytics**: Provides feedback on formatting, structure, and readability.
- **Fast Processing**: Powered by Groq Cloud API for lightning-fast analysis.

## 🛠️ Tech Stack
- **Backend:** Python (FastAPI / Flask)
- **AI Engine:** Groq Cloud API
- **Frontend:** HTML5, CSS3, JavaScript

## 📁 Project Structure
```text
AI-RESUME-ATS-SYSTEM/
│
├── backend/          # API services and core AI logic
├── frontend/         # UI templates and styling
├── .env              # Environment variables (API Keys)
├── .gitignore        # Files excluded from Git tracking
└── requirements.txt  # Project dependencies
```

## 🔄 How It Works (Workflow)

Here is the complete step-by-step working of the AI Resume ATS System:

```text
[User Uploads Resume] ➡️ [Enters Job Description] ➡️ [AI Extraction & Parsing] ➡️ [ATS Scoring & Match Analysis] ➡️ [Interactive Dashboard Output]
```

### 1️⃣ Step 1: User Input (Frontend)
- User dashboard par aakar apna **Resume (PDF/Docx format)** upload karta hai.
- Usi ke sath diye gaye text area mein woh targeted **Job Description (JD)** ko paste karta hai.

### 2️⃣ Step 2: Data Parsing (Backend)
- Backend system resume se saara text extract karta hai.
- Python scripts pure text ko clean aur format karti hain taaki AI use sahi se samajh sake.

### 3️⃣ Step 3: AI Processing (Groq API)
- Extracted resume aur job description dono ko secure tarike se **Groq Cloud AI Model** ke paas bheja jata hai.
- AI dono text ko compare karta hai aur niche di gayi cheezein calculate karta hai:
  - **Match Score (%)**
  - **Missing Keywords & Skills**
  - **Profile Summary Improvement Tips**

### 4️⃣ Step 4: JSON Output Generation
- AI se aane wale raw response ko backend ek structured **JSON format** mein convert karta hai taaki data breakdown aasan ho sake.

### 5️⃣ Step 5: Final Result Display (User View)
- Frontend par user ko ek clean, visually appealing format mein output dikhaya jata hai:
  - **Progress Bar:** Jo ATS Score dikhati hai (e.g., 75% Match).
  - **Bullet Points:** Jo batate hain ki kaunse keywords resume mein missing hain.
  - **Verdict:** Ek professional advice ki resume mein kya badlav karne chahiye.
