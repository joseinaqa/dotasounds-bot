from app.models import Audio
import logging
from bs4 import BeautifulSoup
import requests


domain = 'https://dota2.gamepedia.com'

def make_entry(li):
    source_el = li.find('source')

    if not source_el:
        return None

    src = source_el['src']
    title = ''.join(filter(lambda x: not x.name, li.contents)).strip()

    return Audio(src=src, title=title)

def collect_sounds(url):
    logging.info(f'Scraping {url}...')

    website_request = requests.get(f'{domain}{url}', timeout=5)
    website_content = BeautifulSoup(website_request.content, 'html.parser')
    page_content = website_content.find(class_='mw-parser-output')

    for table in page_content.findAll('table'):
        table.decompose()

    entries = map(make_entry, page_content.findAll('li'))

    Audio.objects.bulk_create(filter(bool, entries))

    logging.info(f'Scraping {url} done!')


def scrape():
    logging.info('Clearing...')
    Audio.objects.all().delete()

    logging.info('Scraping...')

    website_request = requests.get(f'{domain}/Category:Responses', timeout=5)
    website_content = BeautifulSoup(website_request.content, 'html.parser')
    urls = list(map(
        lambda a: a['href'],
        website_content
        .find(class_='mw-category')
        .findAll('a')
    ))

    for url in urls:
        collect_sounds(url)


# TODO: Make scraping automatic

# def schedule_scraping():
    # schedule.every().day.at('08:00').do(scrape)

    # while True:
    #     schedule.run_pending()
