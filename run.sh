#!/bin/bash

pip install --upgrade pip > /dev/null 2>&1

echo "Beginning Telethon test"
pip install --force-reinstall https://github.com/lonamiwebs/telethon/archive/a2926b5.zip cryptg==0.5.0.post0 > /dev/null 2>&1
python scripts/t1.py
pip uninstall -y telethon cryptg > /dev/null 2>&1

echo "Beginning Pyrogram test"
pip install --force-reinstall https://github.com/TelegramPlayGround/Pyrogram/archive/26c2d73.zip https://github.com/TelegramPlayGround/pyrogram-tgcrypto/archive/10142c3.zip > /dev/null 2>&1
python scripts/p2.py
pip uninstall -y pyrotgfork pytgcrypto > /dev/null 2>&1
