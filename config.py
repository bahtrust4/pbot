import os
import sys
import json

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")


if not os.path.exists(CONFIG_PATH):
    print(f'{CONFIG_PATH} not found')
    sys.exit(1)


configdata = json.load(open(CONFIG_PATH, 'r'))

INCLUDED_LOGGING_USER_NAMES = configdata['INCLUDED_LOGGING_USER_NAMES']
ALLOWED_USER_NAMES = configdata['ALLOWED_USER_NAMES']
OPENAI_API_KEY = configdata.get('OPENAI_API_KEY', None)

TELEGRAM_TOKEN = configdata['TELEGRAM_TOKEN']

REPLICATE_API_KEY = configdata.get('REPLICATE_API_KEY', None)

YT_DL_DIR = configdata.get('YT_DL_DIR', None)
YT_DL_URL = configdata.get('YT_DL_URL', None)

NGROK_TUNNEL_URL = configdata['NGROK_TUNNEL_URL']
