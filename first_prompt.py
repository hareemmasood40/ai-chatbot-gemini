import os
from dotenv import load_dotenv
from google import genai

load_dotenv("03_projects/ai_chatbot_project/.env")

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Explain what a decision tree is, in one simple sentence."
)

print(response.text)
