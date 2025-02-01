import logging
import os
from datetime import datetime
from telethon import __version__
from telethon.sessions import MemorySession
from telethon.sync import TelegramClient


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.StreamHandler()
    ]
)


TG_API_ID = int(os.environ.get("TG_API_ID", "6"))
TG_API_HASH = os.environ.get("TG_API_HASH", "")
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
TG_FLOOD_SLEEP_THRESHOLD = int(os.environ.get("TG_FLOOD_SLEEP_THRESHOLD", "10"))
TG_MESSAGE_LINK = os.environ.get("TG_MESSAGE_LINK", "")


app = TelegramClient(
    session=MemorySession(),
    api_id=TG_API_ID,
    api_hash=TG_API_HASH,
    flood_sleep_threshold=TG_FLOOD_SLEEP_THRESHOLD
)
print(f"Telethon: {__version__}")
app.connect()
app.sign_in(bot_token=TG_BOT_TOKEN)

_, _, _, chat_id, s_message_id = TG_MESSAGE_LINK.split("/")

t1 = datetime.now()
message = app.get_messages(entity=chat_id, ids=int(s_message_id))
t2 = datetime.now()
filename = message.download_media()
t3 = datetime.now()
print(f"Downloaded in {(t3 - t2).seconds} seconds")
t4 = datetime.now()
app.send_file(
    entity=chat_id,
    file=filename,
    caption="Telethon",
    reply_to=message
)
t5 = datetime.now()
print(f"Uploaded in {(t5 - t4).seconds} seconds")
os.remove(filename)

app.disconnect()
