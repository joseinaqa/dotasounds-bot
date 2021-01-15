import logging
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import django
django.setup()

from app.scrape import scrape
from app.bot_server import start_bot

logging.basicConfig(level=logging.DEBUG)


scrape()
start_bot()
