import fitz
from openai import OpenAI
import os # <-- Import os

# Load the key directly from the environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found. Make sure it's set in your .env file.")

client = OpenAI(api_key=OPENAI_API_KEY)

# ... (the rest of the file is unchanged)
def extract_text_from_pdf(file_path: str) -> str:
    """Opens a PDF and extracts all text content."""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def analyze_cv_with_ai(cv_text: str) -> str:
    """
    Sends the extracted CV text to the AI for analysis.
    """
    if not cv_text:
        return "Could not read text from the document."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert career coach. You are analyzing a user's CV. Provide a concise analysis covering these three points: 1. Key Strengths, 2. Areas for Improvement, and 3. Three concrete, actionable suggestions for the user to enhance their profile or skills. Format your response clearly using markdown."
                },
                {
                    "role": "user",
                    "content": f"Here is the text from my CV:\n\n{cv_text}"
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error contacting OpenAI: {e}")
        return "There was an error analyzing the document with the AI."