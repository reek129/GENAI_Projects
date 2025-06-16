# 🤖 Telegram Chatbot using OpenAI

A feature‑rich Telegram bot that leverages OpenAI (GPT‑3.5, GPT‑4) to generate conversational, context‑aware responses. Designed for easy deployment and real‑world usage.

---

## 🌟 Highlights

- **Telegram Bot Integration**: Built on `python-telegram-bot` / `aiogram`  
- **GPT‑Powered**: Chat completions via OpenAI’s GPT models  
- **Prompt Engineering**: Structured prompts to maintain context and user tone  
- Supports both **polling** and **webhook** mechanisms  
- Includes robust **error handling** and retries  
- **Modular design**: Ideal for enhancements like media handling or session memory

---

## 🏗 Architecture Diagram

User → Telegram (Front-End) → Backend (calls OpenAI API) → LLM → Response → Backend → Telegram → User



## Add credentials (Create a .env file:)
OPENAI_API_KEY=your-openai-api-key
TELEGRAM_BOT_TOKEN=your-telegram-bot-token

## Install requirements
pip install -r requirements.txt

## Run 
python main.py
