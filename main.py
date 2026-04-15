# main.py
from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PasswordHashInvalid, PhoneCodeExpired, FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, BOT_NAME
from shared import user_data, user_clients
from userbot import setup_userbot_handlers

bot = Client("login_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    welcome_text = (
        f"<b>🚀 {BOT_NAME} Sistemine Hoş Geldiniz</b>\n"
        "──────────────────────\n"
        "<code>Hesabınıza bağlanmak için aşağıdaki butona basın.</code>"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚡ Kurulumu Başlat", callback_data="start_login")],
        [InlineKeyboardButton("📜 Komutlar", callback_data="show_commands")]
    ])
    msg = await client.send_message(message.chat.id, welcome_text, reply_markup=buttons)
    user_data[message.chat.id] = {"main_msg_id": msg.id, "step": None}

# (Giriş işlemleri, Callback ve Login mantığı burada devam eder - Önceki kodun aynısıdır)
# ... [Buraya önceki main.py içerisindeki callback_handler ve login_logic fonksiyonlarını eklemelisin] ...

if __name__ == "__main__":
    print(f"--- {BOT_NAME} ÇALIŞIYOR ---")
    bot.run()
