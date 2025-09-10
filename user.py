from telethon import TelegramClient, events
import requests

# Telegram API bilgilerin
api_id = 1234567
api_hash = "abcdef1234567890"
client = TelegramClient("session", api_id, api_hash)

# HuggingFace ücretsiz token (https://huggingface.co/settings/tokens)
HF_TOKEN = ""

async def get_ai_answer(soru):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": soru}
    response = requests.post(
        "https://api-inference.huggingface.co/models/google/flan-t5-base",
        headers=headers,
        json=payload
    )
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return "⚠️ Yapay zeka servisine bağlanamadım."

@client.on(events.NewMessage(pattern=r"\.artz (.+)"))
async def handler(event):
    soru = event.pattern_match.group(1)
    await event.edit("🤖 Düşünüyorum...")
    try:
        cevap = await get_ai_answer(soru)
        await event.edit(cevap)
    except Exception as e:
        await event.edit(f"❌ Hata: {str(e)}")

print("✅ Userbot çalışıyor...")
client.start()
client.run_until_disconnected()
