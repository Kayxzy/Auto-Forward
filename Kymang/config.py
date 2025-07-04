#Kymang

import os

from dotenv import load_dotenv

load_dotenv(".env")



BOT_TOKEN = os.environ.get("BOT_TOKEN", "6828449IcN9Xo")
API_ID = int(os.environ.get("API_ID", "207449"))
API_HASH = os.environ.get("API_HASH", "ca6822288826f85667a097c0281c")
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://db.net/?retryWrites=true&w=majority")
ADMINS = [int(x) for x in (os.environ.get("ADMINS", "1225634").split())]
MEMBER = [int(x) for x in (os.environ.get("MEMBER", "160").split())]
LOG_GRP = int(os.environ.get("LOG_GRP", "-100717817"))
BOT_ID = int(os.environ.get("BOT_ID", "28449937"))

KITA = [int(x) for x in (os.environ.get("KITA", "1177634").split())]
