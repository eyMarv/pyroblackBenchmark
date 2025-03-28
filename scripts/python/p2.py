import asyncio
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

import logging
import os
from datetime import datetime
from json import dumps
from pyrogram import Client, __version__
from pyrogram.raw.all import layer


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
TG_SESSION = os.environ.get("TG_SESSION", None)
if TG_SESSION == "nil":
    TG_SESSION = None
TG_MESSAGE_LINK = os.environ.get("TG_MESSAGE_LINK", "")


async def main():
    d = {}
    # bot account
    logging.warning("--- STARTING BOT BENCHMARK ---")
    async with Client(
        name="my_bot",
        api_id=TG_API_ID,
        api_hash=TG_API_HASH,
        sleep_threshold=TG_FLOOD_SLEEP_THRESHOLD,
        no_updates=True,
        bot_token=TG_BOT_TOKEN
    ) as app:
        app.upload_boost = True

        d["version"] = __version__
        d["layer"] = layer

        chat_id, s_message_id = TG_MESSAGE_LINK.split("/")

        t1 = datetime.now()
        message = await app.get_messages(chat_id=chat_id, message_ids=int(s_message_id))
        d["file_size"] = message.document.file_size
        t2 = datetime.now()
        filename = await message.download()
        t3 = datetime.now()
        d["download"] = {
            "start_time": t2.timestamp(),
            "end_time": t3.timestamp(),
            "time_taken": (t3 - t2).seconds
        }
        t4 = datetime.now()
        await app.send_document(
            chat_id=message.chat.id,
            document=filename,
            caption="Pyroblack bot",
            reply_to_message_id=message.id
        )
        t5 = datetime.now()
        d["upload"] = {
            "start_time": t4.timestamp(),
            "end_time": t5.timestamp(),
            "time_taken": (t5 - t4).seconds
        }
        os.remove(filename)
    

    # user account
    logging.warning("--- STARTING USER BENCHMARK ---")
    async with Client(
        name="my_account",
        session_string=TG_SESSION,
        api_id=TG_API_ID,
        api_hash=TG_API_HASH,
        sleep_threshold=TG_FLOOD_SLEEP_THRESHOLD,
        no_updates=True,
    ) as app:
        app.upload_boost = True
        chat_id, s_message_id = TG_MESSAGE_LINK.split("/")

        t1 = datetime.now()
        message = await app.get_messages(chat_id=chat_id, message_ids=int(s_message_id))
        t2 = datetime.now()
        filename = await message.download()
        t3 = datetime.now()
        d["download"]["time_taken"] = (int(d["download"]["time_taken"]) + int((t3 - t2).seconds)) / 2
        t4 = datetime.now()
        await app.send_document(
            chat_id=message.chat.id,
            document=filename,
            caption="Pyroblack user",
            reply_to_message_id=message.id
        )
        t5 = datetime.now()
        d["upload"]["time_taken"] = (int(d["download"]["time_taken"]) + int((t5 - t4).seconds)) / 2
        os.remove(filename)
    print(dumps(d, indent=2))


# We need a loop to work with
loop = asyncio.get_event_loop()
# Then, we need to run the loop with a task
loop.run_until_complete(main())
