from telethon import TelegramClient, events

# Buraya kendi api_id ve api_hash değerlerini yaz
api_id = 21883581
api_hash = "c3b4ba58d5dada9bc8ce6c66e09f3f12"

client = TelegramClient("session", api_id, api_hash)

@client.on(events.NewMessage(pattern=r"\.artz (.+)"))
async def handler(event):
    komut = event.pattern_match.group(1).lower()

    if komut == "naber":
        await event.edit("İyiyim sen nasılsın? 😄")
    else:
        await event.edit(f"Sen dedin: {komut}")

print("✅ Userbot çalışıyor...")
client.start()
client.run_until_disconnected()
