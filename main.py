import os
import yt_dlp
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream.quality import HighQualityAudio

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("musicbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(app)

playlist = []

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply("🎧 هلا بيك\nاكتب شغل واسم الاغنية")

@app.on_message(filters.regex("^شغل"))
async def play(_, message):

    query = message.text.replace("شغل ", "")

    if not query:
        return await message.reply("اكتب اسم الاغنية")

    ydl_opts = {
        "format": "bestaudio",
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]
        url = info["url"]

    playlist.append(url)

    chat_id = message.chat.id

    await call_py.join_group_call(
        chat_id,
        InputAudioStream(url, HighQualityAudio())
    )

    await message.reply(f"🎵 يتم التشغيل:\n{info['title']}")

@app.on_message(filters.regex("^اسكت"))
async def stop(_, message):

    await call_py.leave_group_call(message.chat.id)
    playlist.clear()

    await message.reply("🛑 تم ايقاف التشغيل")

@app.on_message(filters.regex("^تخطي"))
async def skip(_, message):

    if playlist:
        playlist.pop(0)

    await message.reply("⏭ تم التخطي")

app.start()
call_py.start()
app.idle()
