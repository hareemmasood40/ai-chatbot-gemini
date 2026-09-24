# Simple AI Chatbot

A command-line chatbot that talks to a real AI model (Google's Gemini) — my first hands-on
project working directly with LLMs (Large Language Models), moving from data analysis into
AI engineering.

## What it does
Type a question, get a real AI-generated answer back, in a continuous conversation loop —
type `quit` to exit. The chatbot **remembers earlier messages** in the same session (using
the Gemini API's built-in chat-session feature), so you can ask natural follow-up questions
like "what's the population of that city?" after asking about a capital.

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

## A note on free-tier reliability
Even with retries in place, Google's free AI tier can get genuinely overloaded at busy times
(paid tiers get priority). This isn't something code alone can fully solve — it's a real
constraint of building on top of free-tier AI services, worth knowing as an AI Engineer
rather than something to be surprised by.

## What I'd do next
- Add a simple system prompt to give the chatbot a specific personality or role
- Build a small web interface instead of the command line
