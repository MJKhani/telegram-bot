import telebot
import schedule
import time
import os
import threading
import datetime

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

def save_user(user_id):
    with open("users.txt", "a") as f:
        f.write(str(user_id) + "\n")

def load_users():
    try:
        with open("users.txt", "r") as f:
            return [int(x.strip()) for x in f]
    except:
        return []

@bot.message_handler(commands=['start'])
def start(msg):
    user_id = msg.chat.id
    save_user(user_id)
    bot.send_message(user_id, "سلام! شما ثبت شدید ✔️")

def send_scheduled_message():
    for uid in load_users():
        try:
            bot.send_message(uid, "🔔 پیام برنامه‌ریزی شده ماهانه ارسال شد!")
        except:
            pass

schedule.every().day.at("06:30").do(send_scheduled_message)

def scheduler_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=scheduler_loop).start()

def monthly_scheduler():
    while True:
        now = datetime.datetime.utcnow()
        day = now.day
        current_time = now.strftime("%H:%M")
        if day in [28, 29] and current_time == "08:30":
            send_scheduled_message()
            time.sleep(70)
        time.sleep(1)

threading.Thread(target=monthly_scheduler).start()

bot.infinity_polling()
