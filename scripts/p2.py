import os
from datetime import datetime
from pyrogram import Client, __version__
from pyrogram.types import ReplyParameters

TG_API_ID = int(os.environ.get("TG_API_ID", "6"))
TG_API_HASH = os.environ.get("TG_API_HASH", "")
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
TG_FLOOD_SLEEP_THRESHOLD = int(os.environ.get("TG_FLOOD_SLEEP_THRESHOLD", "10"))
TG_MESSAGE_LINK = os.environ.get("TG_MESSAGE_LINK", "")

app = Client(
    name="my_account",
    in_memory=True,
    api_id=TG_API_ID,
    api_hash=TG_API_HASH,
    sleep_threshold=TG_FLOOD_SLEEP_THRESHOLD,
    bot_token=TG_BOT_TOKEN
)
print(f"Pyrogram: {__version__}")
app.start()

t1 = datetime.now()
message = app.get_messages(link=TG_MESSAGE_LINK)
t2 = datetime.now()
filename = message.download()
t3 = datetime.now()
print(f"Downloaded in {(t3 - t2).seconds} seconds")
t4 = datetime.now()
app.send_document(
    chat_id=message.chat.id,
    document=filename,
    caption="Pyrogram",
    reply_parameters=ReplyParameters(
        message_id=message.id
    )
)
t5 = datetime.now()
print(f"Uploaded in {(t5 - t4).seconds} seconds")
os.remove(filename)

app.stop()
