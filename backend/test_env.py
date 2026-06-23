import os
from dotenv import load_dotenv

load_dotenv()
print("--- ENVIRONMENT TEST ---")
print(f"GROQ_API_KEY found: {os.getenv('GROQ_API_KEY') is not None}")
print(f"Key starts with: {str(os.getenv('GROQ_API_KEY'))[:4]}")
