import os
from pathlib import Path


GROQ_API_KEY = gsk_xxxx
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Load .env explicitly if available
try:
    from dotenv import load_dotenv
    _ENV_PATH = Path(__file__).resolve().parents[2] / '.env'
    load_dotenv(_ENV_PATH)
except ImportError:
    pass

# API metadata
APP_TITLE = 'ATS RESUME ANALYZER API'
APP_VERSION = '1.0.0'
APP_DESCRIPTION = 'analyse resumes against job description using nlp + ml'

# Localhost को भी जोड़ा गया है ताकि आपकी लोकल स्ट्रीमलिट ऐप ब्लॉक न हो
ALLOWED_ORIGINS = [
    'https://appapppy-ktwxupi73vqhjzweksze9d.streamlit.app/',
    'http://localhost:8501',
    'http://127.0.0.1:8501'
]  

# File constraints
MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# Supported MIME types and their short names
SUPPORTED_MIME_TYPES = {
    'application/pdf': 'pdf',
    'application/msword': 'doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
}

SUPPORTED_EXTENSIONS = {'.pdf', '.doc', '.docx'}

SPACY_MODEL_PRIMARY = "en_core_web_md"
SPACY_MODEL_SECONDARY = "en_core_web_sm"
SENTENCE_TRANSFORMER_MODEL = os.getenv("SENTENCE_TRANSFORMER_MODEL", "all-MiniLM-L6-v2")

# Score component weights
SCORE_WEIGHTS = {
    "formatting": 20, "keywords": 25, "content": 25,
    "skill_validation": 15, "ats_compatibility": 15,
}

JD_KEYWORD_WEIGHT = 0.6
JD_SEMANTIC_WEIGHT = 0.4

# Supabase Credentials
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://wqjxgzlgkkesorreqndd.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indxanhnemxna2tlc29ycmVxbmRkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MjA1MzUxNSwiZXhwIjoyMDk3NjI5NTE1fQ.Jom6oXrmd2-w3w3FcCJK-cWRMc1Q4-5pL87aMWWmHLM')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indxanhnemxna2tlc29ycmVxbmRkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODIwNTM1MTUsImV4cCI6MjA5NzYyOTUxNX0.2hnYhcYrXiRpkvXizJf-CtBXMvAomhZN8gJt82n397U')
SUPABASE_JWT_SECRET = os.getenv('SUPABASE_JWT_SECRET','0LYwji6v7/9pXRkuncxRb5LGgIGCrGzIi3T/8BEBhvu/pVMEZYcugZdeEnIW2wrW+xkf/u5p3KDagwmmkjIDDg==')
