import logging
import os
from datetime import datetime
from json import dumps
from telethon import __version__
from telethon.sessions import MemorySession
from telethon.sync import TelegramClient
from telethon.tl.alltlobjects import LAYER


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


d = {}

app = TelegramClient(
    session=MemorySession(),
    api_id=TG_API_ID,
    api_hash=TG_API_HASH,
    flood_sleep_threshold=TG_FLOOD_SLEEP_THRESHOLD,
    receive_updates=False
)
d["version"] = __version__
d["layer"] = LAYER
app.connect()
app.sign_in(bot_token=TG_BOT_TOKEN)

_, _, _, chat_id, s_message_id = TG_MESSAGE_LINK.split("/")

t1 = datetime.now()
message = app.get_messages(entity=chat_id, ids=int(s_message_id))
d["file_size"] = message.file.size
t2 = datetime.now()
filename = message.download_media()
t3 = datetime.now()
d["download"] = {
    "start_time": t2.timestamp(),
    "end_time": t3.timestamp(),
    "time_taken": (t3 - t2).seconds
}
t4 = datetime.now()
app.send_file(
    entity=chat_id,
    file=filename,
    caption="Telethon",
    force_document=True,
    reply_to=message
)
t5 = datetime.now()
d["upload"] = {
    "start_time": t4.timestamp(),
    "end_time": t5.timestamp(),
    "time_taken": (t3 - t2).seconds
}
os.remove(filename)

app.disconnect()

print(dumps(d, indent=2))
