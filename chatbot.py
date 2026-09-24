import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv("03_projects/ai_chatbot_project/.env")

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

chat = client.chats.create(model="gemini-flash-lite-latest")

print("Simple AI Chatbot (with memory) — type 'quit' to exit\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    for attempt in range(3):
        try:
            response = chat.send_message(user_input)
            print("AI:", response.text)
            break
        except Exception:
            print(f"(attempt {attempt + 1} failed, retrying in 3 seconds...)")
            time.sleep(3)
    else:
        print("AI: Sorry, the service is unavailable right now.")
