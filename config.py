import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

REMNA_URL = os.getenv("REMNA_URL")
REMNA_TOKEN = os.getenv("REMNA_TOKEN")

ADMINS = list(map(int, os.getenv("ADMINS").split(",")))

TAG = os.getenv("TAG")
