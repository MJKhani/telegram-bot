ربات اعلانات و...  

با امکانات:

ارسال اعلان در روزهای مشخص و ساعت مشخص شده به کاربران عضو ربات

ارسال پیام توسط ادمین ربات به همه کاربران یا به یک کاربر خاص با دستور /send

نکته برای ارسال به کاربر خاص ابتدا باید (@ایدی عددی) را وارد کرد به طور مثال:

@123456 سلام خوش امدید!

ارسال عکس توسط کاربران با دستور /photo

اعلان عضو جدید برای ادمین

نمایش نام کاربری کاربران

نمایش ایدی عددی کاربران

نمایش یوزرنیم کاربران

همچنین با دستور /users نیز به صورت یکجا تمام کاربران با مشخصات کامل برایتان قابل نمایش است

تمام موارد را نیز میتوان در فایل bot.py ادیت و شخصی سازی کرد.


دستورات نصب و راه اندازی به صورت کامل:

ابتدا در ترمینال هاست به مسیر فایل اپلود شده بروید:

cd /home/Username/public_html/telegram-bot

دسترسی دادن به فایل:

chmod +x start_bot.sh

مشاهده ورژن نصب شده:

python3 --version

python3 -m pip --version

نصب کتابخانه:

pip install --user -r requirements.txt

python3 -m pip install --user -r requirements.txt

در صورت عدم نصب با دستور بالا:

python3 -m pip install --user "pyTelegramBotAPI<4.0" schedule

python3 -m pip install --user pyTelegramBotAPI schedule

مشاهده ورژن و حذف:

python3 -m pip show pyTelegramBotAPI

python3 -m pip show schedule

python3 -m pip uninstall pyTelegramBotAPI

راه اندازی ربات:

nohup python3 bot.py & 

python3 bot.py

متوقف کردن ربات:

pkill -f bot.py

کرون جاب:

Minute: 0
Hour: 0
Day: *
Month: *
Weekday: *

/home/anonymou/public_html/telegram-bot/start_bot.sh
