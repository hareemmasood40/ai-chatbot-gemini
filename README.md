# Simple AI Chatbot

A command-line chatbot that talks to a real AI model (Google's Gemini) — my first hands-on
project working directly with LLMs (Large Language Models), moving from data analysis into
AI engineering.

## What it does
Type a question, get a real AI-generated answer back, in a continuous conversation loop —
type `quit` to exit.

## Tools
Python, Google Gemini API (`google-genai`), `python-dotenv`

## How it works
1. Loads a secret API key safely from a `.env` file (never hardcoded, never committed to
   GitHub — protected by `.gitignore`)
2. Sends whatever the user types to Google's Gemini model via the API
3. Prints the model's response
4. Repeats until the user types `quit`

## Real problems I ran into and fixed
- **A deprecated model name.** My first model choice (`gemini-2.5-flash`) had been retired
  ("no longer available to new users"). Fixed by reading the actual error message, which
  named the replacement model.
- **Temporary service outages (503 "high demand").** The AI service was genuinely
  unavailable at times — not a bug in my code. I added:
  - A `try/except` block so one failed request doesn't crash the whole chatbot
  - An automatic retry (3 attempts, with a short wait between each) before giving up gracefully
  - Switched to `gemini-flash-lite-latest`, which turned out to be more reliably available
- **API key security.** Since my GitHub repos are public, I store the key in a `.env` file
  that's explicitly excluded from Git via `.gitignore` — it never leaves my machine.

## What I'd do next
- Add a simple system prompt to give the chatbot a specific personality or role
- Build a small web interface instead of the command line
- Add conversation memory so it remembers earlier messages in the same session
