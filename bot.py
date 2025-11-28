import telebot
import schedule
import time
import threading
import datetime
import os
import sys
from telebot import types

# -------------------------------
# ⚡ توکن ربات
# -------------------------------
TOKEN = "Fake_Token"  # <-- توکن خودت را اینجا قرار بده
bot = telebot.TeleBot(TOKEN)

# -------------------------------
# 👑 ادمین‌ها
# -------------------------------
ADMINS = [85015457]   # آیدی عددی خودت

# -------------------------------
# کاربران مجاز برای ارسال عکس
# -------------------------------
photo_waiting = {}  # user_id : True/False

# -------------------------------
# ذخیره و بارگذاری کاربران
# -------------------------------
def save_user(user_id):
    with open("users.txt", "a") as f:
        f.write(str(user_id) + "\n")

def load_users():
    try:
        with open("users.txt", "r") as f:
            return [int(x.strip()) for x in f]
    except:
        return []

# -------------------------------
# دستور /start + اعلام به ادمین
# -------------------------------
@bot.message_handler(commands=['start'])
def start(msg):
    user_id = msg.chat.id
    username = msg.from_user.username or "ندارد"
    first_name = msg.from_user.first_name or "ندارد"

    users = load_users()

    if user_id not in users:
        save_user(user_id)

        # اطلاع به ادمین
        for admin in ADMINS:
            bot.send_message(
                admin,
                f"👤 کاربر جدید عضو شد:\n"
                f"🆔 ID: {user_id}\n"
                f"📛 نام: {first_name}\n"
                f"🔗 یوزرنیم: @{username}"
            )

    # پیام خوش‌آمد
    bot.send_message(
        user_id,
        """سلام🌹
خوش آمدید❤️
شما در ربات اعلانات پرداخت ماهیانه شارژ پنل نمایندگان ثبت شدید✅
این ربات به صورت خودکار در روزهای 28 و 29 هر ماه میلادی جهت یادآوری پرداخت برای شما اعلان ارسال میکند💯
و
در آینده امکانات بیشتری نیز اضافه خواهد شد."""
    )

# -------------------------------
# پیام زمان‌بندی‌شده
# -------------------------------
def send_scheduled_message():
    users = load_users()
    for uid in users:
        try:
            bot.send_message(uid,
"""🔔نماینده عزیز سلام
⏰ زمان سر رسید تمدید پنل فرار رسیده
❌لطفا جهت جلوگیری از قطع سرویس خود
هرچه سریعتر قبلا از تاریخ 30ام پنل خود را تمدید و
عکس رسید را در اینجا با زدن دکمه /photo  ارسال کنید
یا اینکه برای ادمین ارسال کنید:
https://t.me/AnonymousVps011Admin
""")
        except Exception as e:
            print(f"خطا در ارسال به {uid}: {e}")

# روزانه (اختیاری)
schedule.every().day.at("06:30").do(send_scheduled_message)

def scheduler_loop():
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            print("خطا در scheduler_loop:", e)
        time.sleep(1)

threading.Thread(target=scheduler_loop, daemon=True).start()

# -------------------------------
# زمان‌بندی ماهانه - 28 و 29 ساعت 08:30 UTC
# -------------------------------
def monthly_scheduler():
    while True:
        try:
            now = datetime.datetime.utcnow()
            if now.day in [28, 29] and now.strftime("%H:%M") == "12:00":
                send_scheduled_message()
                time.sleep(70)
        except Exception as e:
            print("خطا در monthly_scheduler:", e)
        time.sleep(1)

threading.Thread(target=monthly_scheduler, daemon=True).start()

# -------------------------------------------------
# 🟦 ارسال پیام دستی /send
# -------------------------------------------------
@bot.message_handler(commands=['send'])
def send_message_start(msg):
    user_id = msg.chat.id
    if user_id not in ADMINS:
        bot.send_message(user_id, "❌ شما اجازه استفاده از این بخش را ندارید.")
        return

    markup = types.ForceReply(selective=True)
    bot.send_message(user_id, "لطفاً متن پیام خود را وارد کنید:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.reply_to_message and "لطفاً متن پیام" in m.reply_to_message.text)
def send_message_text(msg):
    user_id = msg.chat.id
    if user_id not in ADMINS:
        return

    text_to_send = msg.text

    # ارسال به کاربر خاص
    if text_to_send.startswith("@"):
        try:
            parts = text_to_send.split(" ", 1)
            target_id = int(parts[0][1:])
            bot.send_message(target_id, parts[1])
            bot.send_message(user_id, "پیام ارسال شد ✅")
        except:
            bot.send_message(user_id, "❌ خطا در ارسال پیام")
    else:
        # ارسال به همه کاربران
        for uid in load_users():
            try:
                bot.send_message(uid, text_to_send)
            except:
                pass
        bot.send_message(user_id, "پیام به همه کاربران ارسال شد ✅")

# -------------------------------------------------
# 🟦 دکمه ارسال عکس (/photo)
# -------------------------------------------------
@bot.message_handler(commands=['photo'])
def request_photo(msg):
    user_id = msg.chat.id
    # فعال کردن اجازه ارسال عکس برای کاربر
    photo_waiting[user_id] = True
    # پیام راهنما
    bot.send_message(user_id, "✅ خیلیم عالی! حالا لطفاً عکس رسیدت رو ارسال کنید.")

# -------------------------------------------------
# 🟦 دریافت عکس کاربران + ارسال به ادمین (با محدودیت)
# -------------------------------------------------
@bot.message_handler(content_types=['photo'])
def handle_photo(msg):
    user_id = msg.chat.id

    # ❌ اگر کاربر اجازه ندارد
    if not photo_waiting.get(user_id, False):
        bot.send_message(user_id, "❌ ابتدا دستور /photo را بزنید و سپس رسید خود را ارسال کنید.")
        return

    # ✔ بعد از یکبار ارسال، فلگ خاموش می‌شود
    photo_waiting[user_id] = False

    username = msg.from_user.username or "ندارد"
    first_name = msg.from_user.first_name or "ندارد"

    try:
        file_id = msg.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        os.makedirs("photos", exist_ok=True)
        file_path = f"photos/{user_id}_{file_id}.jpg"

        with open(file_path, "wb") as f:
            f.write(downloaded_file)

        bot.send_message(user_id, "✅ عکس شما ارسال شد!")

        # ارسال به ادمین
        for admin in ADMINS:
            with open(file_path, "rb") as p:
                bot.send_photo(
                    admin,
                    p,
                    caption=f"📸 عکس جدید از کاربر:\n🆔 ID: {user_id}\n👤 نام: {first_name}\n🔗 یوزرنیم: @{username}"
                )

    except Exception as e:
        bot.send_message(user_id, f"❌ خطا: {e}")

# -------------------------------------------------
# 🗑 حذف خودکار عکس‌ها
# -------------------------------------------------
def auto_delete_photos(delay=300):
    while True:
        try:
            folder = "photos"
            if os.path.exists(folder):
                for file in os.listdir(folder):
                    fpath = os.path.join(folder, file)
                    if os.path.isfile(fpath) and time.time() - os.path.getmtime(fpath) > delay:
                        os.remove(fpath)
        except Exception as e:
            print("خطا در پاک کردن عکس‌ها:", e)
        time.sleep(60)

threading.Thread(target=auto_delete_photos, daemon=True).start()

# -------------------------------------------------
# 🟦 لیست کاربران /users
# -------------------------------------------------
@bot.message_handler(commands=['users'])
def list_users(msg):
    if msg.chat.id not in ADMINS:
        bot.send_message(msg.chat.id, "❌ اجازه ندارید.")
        return

    users = load_users()
    if not users:
        bot.send_message(msg.chat.id, "هیچ کاربری وجود ندارد.")
        return

    text = "👥 لیست کاربران:\n\n"
    for uid in users:
        try:
            info = bot.get_chat(uid)
            text += f"ID: {uid}\nUsername: @{info.username}\nName: {info.first_name}\n\n"
        except:
            text += f"ID: {uid}\n❌ خطا در دریافت اطلاعات\n\n"

    for chunk in [text[i:i+3000] for i in range(0, len(text), 3000)]:
        bot.send_message(msg.chat.id, chunk)

# -------------------------------
# اجرای ربات
# -------------------------------
def run_bot_forever():
    while True:
        try:
            print("ربات فعال شد ...")
            bot.infinity_polling()
        except Exception as e:
            print("خطا:", e)
            time.sleep(5)

run_bot_forever()
