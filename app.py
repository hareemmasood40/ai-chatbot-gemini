import os
import json
import uuid
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv("03_projects/ai_chatbot_project/.env")

# Locally: reads from the .env file. When deployed on Streamlit Cloud: reads from
# the "Secrets" the app is configured with there (there's no .env file on the server).
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    api_key = st.secrets.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
MODEL = "gemini-flash-lite-latest"
HISTORY_FILE = "03_projects/ai_chatbot_project/chat_history.json"

PERSONALITIES = {
    "Friendly Assistant": "You are a warm, friendly, helpful assistant. Keep answers clear and concise.",
    "Data Analyst Mentor": "You are an experienced Data Analyst mentor. Explain things simply, "
                            "like you're helping a junior analyst, and relate answers to real data work where relevant.",
    "Concise Expert": "You answer as briefly and directly as possible, no fluff, just the key facts.",
}

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot (Gemini)")

# ---------- Persistent storage: multiple saved conversations ----------
def load_all():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"conversations": {}, "current": None}

def save_all(data):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def new_conversation(data):
    conv_id = str(uuid.uuid4())
    data["conversations"][conv_id] = {
        "title": "New Chat",
        "created": datetime.now().strftime("%d %b, %H:%M"),
        "messages": [],
    }
    data["current"] = conv_id
    return conv_id

if "data" not in st.session_state:
    st.session_state.data = load_all()
    if not st.session_state.data["current"] or st.session_state.data["current"] not in st.session_state.data["conversations"]:
        new_conversation(st.session_state.data)
        save_all(st.session_state.data)

data = st.session_state.data

# ---------- Sidebar: settings + conversation list ----------
with st.sidebar:
    st.header("Settings")
    mode = st.radio("Mode", ["Chat", "Summarizer"])
    personality = st.selectbox("Personality", list(PERSONALITIES.keys()))

    st.divider()
    st.header("Conversations")

    if st.button("➕ New Chat", use_container_width=True):
        new_conversation(data)
        save_all(data)
        st.rerun()

    # List past conversations, most recent first
    for conv_id, conv in sorted(data["conversations"].items(), key=lambda kv: kv[1]["created"], reverse=True):
        label = f"{conv['title']}  ·  {conv['created']}"
        is_current = conv_id == data["current"]
        if st.button(("🟢 " if is_current else "") + label, key=conv_id, use_container_width=True):
            data["current"] = conv_id
            save_all(data)
            st.rerun()

current_conv = data["conversations"][data["current"]]

# ---------- Rebuild a chat session from the current conversation's saved messages ----------
chat = client.chats.create(
    model=MODEL,
    config=types.GenerateContentConfig(system_instruction=PERSONALITIES[personality]),
    history=[
        {"role": m["role"], "parts": [{"text": m["text"]}]}
        for m in current_conv["messages"]
    ],
)

# ---------- CHAT MODE ----------
if mode == "Chat":
    for m in current_conv["messages"]:
        with st.chat_message("user" if m["role"] == "user" else "assistant"):
            st.write(m["text"])

    user_input = st.chat_input("Type a message...")
    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        current_conv["messages"].append({"role": "user", "text": user_input})

        # First message in a chat becomes its title, so it's recognisable in the sidebar
        if current_conv["title"] == "New Chat":
            current_conv["title"] = user_input[:40] + ("..." if len(user_input) > 40 else "")

        try:
            response = chat.send_message(user_input)
            reply = response.text
        except Exception:
            reply = "Sorry, the AI service is unavailable right now. Please try again."

        with st.chat_message("assistant"):
            st.write(reply)
        current_conv["messages"].append({"role": "model", "text": reply})
        save_all(data)

# ---------- SUMMARIZER MODE ----------
else:
    text_to_summarize = st.text_area("Paste text to summarize", height=200)
    if st.button("Summarize"):
        if text_to_summarize.strip():
            try:
                response = client.models.generate_content(
                    model=MODEL,
                    contents=f"Summarize this text in 3-4 short bullet points:\n\n{text_to_summarize}",
                )
                st.subheader("Summary")
                st.write(response.text)
            except Exception:
                st.error("Sorry, the AI service is unavailable right now. Please try again.")
        else:
            st.warning("Paste some text first.")
