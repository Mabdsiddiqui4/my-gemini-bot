import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai
from google.genai import types

# إعداد السجلات لمراقبة البوت
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# المفاتيح الخاصة بك هنا مباشرة
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # or you can add her the TOKEN form BotFather in telegram
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # API from ai stodio

# إعداد الاتصال بخوادم جوجل
client = genai.Client(api_key=GOOGLE_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أنا مساعدك الذكي المدعوم من Gemini. اسألني أي شيء وسأجيبك فوراً!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
            config=types.GenerateContentConfig(
                system_instruction="أنت مساعد ذكي مفيد وتتحدث العربية بطلاقة."
            )
        )
        bot_reply = response.text
    except Exception as e:
        logging.error(f"Error: {e}")
        bot_reply = "عذراً، حدث خطأ أثناء معالجة الطلب. يرجى المحاولة مرة أخرى."

    await update.message.reply_text(bot_reply)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("البوت يعمل الآن بنجاح عبر خوادم Google Gemini...")
    app.run_polling()

if __name__ == '__main__':
    main()
