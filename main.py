import logging
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import django
django.setup()

from app.scrape import schedule_scraping

logging.basicConfig(level=logging.DEBUG)


schedule_scraping()
