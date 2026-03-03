import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "gemini-2.5-flash"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please check your .env file.")
