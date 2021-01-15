import logging
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import django
django.setup()

import threading

from app.scrape import scrape
from app.bot_server import start_bot

logging.basicConfig(level=logging.DEBUG)


threading.Thread(target=scrape)
start_bot()
