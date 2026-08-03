# My Gemini Telegram Bot 🤖

A fully responsive, 100% free Telegram chatbot powered by the **Google Gemini 2.5 Flash** model via Google AI Studio.
The bot is deployed seamlessly on cloud servers to run 24/7 without requiring any local machine resources or downloads.

---

## 🛠️ Step-by-Step Implementation Guide

### Step 1: Secure the API Keys from Google AI Studio
1. Visited [Google AI Studio](https://google.com) and logged in with a Google account.
2. Clicked on **Get API key** and generated a new API key.
3. Copied the key securely to use it during deployment.

### Step 2: Set Up the GitHub Repository
1. Created this GitHub repository to host the source code cloud-side (no local installations needed).
2. Created `requirements.txt` to specify dependencies:
   - `python-telegram-bot`
   - `google-genai`
3. Created the core python script named `hot.py` containing the bot logic.

### Step 3: Secure Secrets & Tokens
To keep sensitive credentials hidden from the public, hardcoded values were replaced with environment variables:
```python
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
```

---

## 🛑 The Challenge We Faced & How We Solved It

### The Problem:
Initially, the bot was planned to be deployed on **Render** using a **Background Worker** instance type.
However, during configuration, we discovered that Render recently deprecated the free tier for Background Workers, requiring a mandatory $7/month starter fee.

### The Solution (100% Free Fix):
We pivoted the architecture to a **Render Web Service** instead, which still offers a completely **Free Tier**. 

To adapt the standard Telegram polling script to a Web Service (which inherently listens for an incoming HTTP web port),
  we applied a clever configuration bypass:
1. Changed the deployment type from Background Worker to **Web Service**.
2. Adjusted the **Start Command** to pass an internal variable:
   ```bash
   python hot.py --port \$PORT
   ```
3. Injected the secret tokens via Render's **Advanced Settings -> Environment Variables** box.

This allowed the bot to initialize flawlessly on Render's free servers, establishing a continuous polling loop with Telegram while remaining completely cost-free!

---

## 🚀 How to Run the Bot

1. Open Telegram and search for your bot username.
2. Click **Start** or type `/start`.
3. Interact with the bot in Arabic or English, and enjoy fast, AI-powered responses!
