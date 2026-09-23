import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv("03_projects/ai_chatbot_project/.env")

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

print("Simple AI Chatbot — type 'quit' to exit\n")

def ask_ai(prompt, attempts=3):
    for i in range(attempts):
        try:
            response = client.models.generate_content(
                model="gemini-flash-lite-latest",
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"(attempt {i+1} failed, retrying in 3 seconds...)")
            time.sleep(3)
    return "Sorry, the AI service is unavailable right now. Please try again later."

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    print("AI:", ask_ai(user_input))
