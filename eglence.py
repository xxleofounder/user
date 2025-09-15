from telethon import events, Button
from bot import client
import asyncio

@client.on(events.NewMessage(pattern="^/eros ?(.*)"))
async def eros(event):
    bot_username = (await client.get_me()).username

    # Grup dışında kullanım kontrolü
    if event.is_private:
        return await event.respond(
            "üᴢɢüɴüᴍ, ʙᴜ ᴋᴏᴍᴜᴛ ɢʀᴜᴘ ᴠᴇʏᴀ ᴋᴀɴᴀʟʟᴀʀ içiɴ ɢᴇçᴇʀʟiᴅiʀ❗️",
            buttons=[[Button.url("➕ ʙᴇɴi ɢʀᴜʙᴀ ᴇᴋʟᴇ", f"https://t.me/{botUserName}?startgroup=true")]],
            reply_to=event.message.id
        )

    # Grup kullanıcılarını al
    participants = [u async for u in client.iter_participants(event.chat_id) if not u.bot and not u.deleted]

    # Eğer yanıt varsa
    if event.reply_to_msg_id:
        replied_msg = await event.get_reply_message()
        target = replied_msg.sender
        user1 = event.sender
        user2 = target
    else:
        # Yanıt yoksa rastgele 2 kişi seç
        if len(participants) < 2:
            return await event.respond("⚠️ ʏᴇᴛᴇʀʟi ᴋᴜʟʟᴀɴɪᴄɪ ʏᴏᴋ!")
        user1, user2 = random.sample(participants, 2)

    # Eros mesajı ve emoji
    emojis = ["💖","💕","💘","💞","💓","💗","💝","💟","❣️"]
    emoji = random.choice(emojis)

    # Aşk mesajı listesi
    love_messages = [
        "**Aşk dolu bir an yaşadınız!** 😍",
        "**Kalpler bir araya geldi** 💞",
        "**Romantik bir sürpriz!** 💖",
        "**Sevgi dolu bir Eros geldi!** 💘",
        "**Kalpler birbirine dokundu** ❤️"
    ]
    love_msg = random.choice(love_messages)

    # Tıklanabilir isimlerle mesaj
    msg_text = f"{emoji} [{user1.first_name}](tg://user?id={user1.id}) ❤️ [{user2.first_name}](tg://user?id={user2.id}) {emoji}\n{love_msg}"

    # Mesajı gönder
    await event.respond(msg_text, reply_to=event.message.id, parse_mode='md')
    
