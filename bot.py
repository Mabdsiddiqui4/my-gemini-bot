import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai
from google.genai import types
#---------
import asyncio
#---------
import http.server
import threading
# دالة لتشغيل سيرفر وهمي لإرضاء منصة Render المجانية
def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
    print(f"Dummy server running on port {port}...")
    httpd.serve_forever()

# تشغيل السيرفر الوهمي في الخلفية قبل بدء البوت
threading.Thread(target=run_dummy_server, daemon=True).start()
#---------------
# إعداد السجلات لمراقبة البوت
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# المفاتيح الخاصة بك هنا مباشرة
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # or you can add her the TOKEN form BotFather in telegram
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # API from ai stodio

# إعداد الاتصال بخوادم جوجل
client = genai.Client(api_key=GOOGLE_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أنا مساعدك الذكي المدعوم من Gemini. اسألني أي شيء وسأجيبك فوراً!")
#معالجة النصوص والصور
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    user_text = update.message.text or update.message.caption or "حلل هذه الصورة واشرح ما فيها بالتفصيل."
    image_bytes = None

    if update.message.photo:
        photo_file = await update.message.photo[-1].get_file()
        image_bytes = await photo_file.download_as_bytearray()
    # ----------------------
  #  await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    # ------------------------
    try:
        # تجهيز محتويات الطلب لجوجل
        contents = [user_text]
        if image_bytes:
            contents.append(
                types.Part.from_bytes(
                    data=bytes(image_bytes),
                    mime_type="image/jpeg"
                )
            )
# this is for gemini recwest
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction="أنت مساعد ذكي مفيد وتتحدث العربية بطلاقة. إذا أرسل المستخدم صورة، فقم بتحليلها بدقة والإجابة بناءً عليها وعلى النص المرفق."
            )
        )
        bot_reply = response.text
    except Exception as e:
        logging.error(f"Error: {e}")
        bot_reply = "عذراً، حدث خطأ أثناء معالجة الطلب. يرجى المحاولة مرة أخرى."

    await update.message.reply_text(bot_reply)

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # بناء وتأمين اتصال بوت التيليجرام   
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler((filters.TEXT | filters.PHOTO) & ~filters.COMMAND, handle_message))
    
    print("البوت يعمل الآن بنجاح عبر خوادم Google Gemini...")
    app.run_polling()

if __name__ == '__main__':
    main()
