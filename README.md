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

🔄 How It Works (Workflow)Here is the complete step-by-step working of the AI Resume ATS System:text[User Uploads Resume] ➡️ [Enters Job Description] ➡️ [AI Extraction & Parsing] ➡️ [ATS Scoring & Match Analysis] ➡️ [Interactive Dashboard Output]
Use code with caution.
1️⃣ Step 1: User Input (Frontend)The user visits the dashboard and uploads their Resume (PDF/Docx format).Along with it, they paste the targeted Job Description (JD) into the provided text area.
2️⃣ Step 2: Data Parsing (Backend)The backend system extracts all the text from the resume.Python scripts clean and format the entire text so that the AI can understand it accurately.
3️⃣ Step 3: AI Processing (Groq API)Both the extracted resume and the job description are securely sent to the Groq Cloud AI Model.The AI compares both texts and calculates the following elements:Match Score (%)Missing Keywords & SkillsProfile Summary Improvement Tips
4️⃣ Step 4: JSON Output GenerationThe backend converts the raw response received from the AI into a structured JSON format for an easy data breakdown.
5️⃣ Step 5: Final Result Display (User View)The output is displayed to the user on the frontend in a clean, visually appealing format:Progress Bar: Displays the ATS Score (e.g., 75% Match).Bullet Points: Highlights which keywords are missing from the resume.Verdict: Provides professional advice on what changes should be made to the resume.
