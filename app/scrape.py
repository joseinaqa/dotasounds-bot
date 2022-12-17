import re
import logging
from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor


def is_subseq(the_seq, the_string):
    rgx = re.compile('.*'.join([re.escape(x) for x in the_seq]))
    return rgx.search(the_string)


def is_hero_searched(query, raw_name):
    name = raw_name.lower()
    return name[0:2] == query[0:2] and is_subseq(query, name)


domain = 'https://dota2.fandom.com'

def make_entry(li, query, name):
    source_el = li.find('source')
    title = ''.join(filter(lambda x: not x.name, li.contents)).strip()

    if not source_el or not is_subseq(query, title.lower()):
        return None

    src = source_el['src']

    return {
        'src': src,
        'title': f'{name}: {title}',
    }

def collect_sounds(hero, query):
    url = hero['url']
    name = hero['name']
    logging.info(f'Scraping {url}...')

    website_request = requests.get(f'{domain}{url}', timeout=5)
    website_content = BeautifulSoup(website_request.content, 'html.parser')
    page_content = website_content.find(class_='mw-parser-output')

    for table in page_content.find_all('table'):
        table.decompose()

    entries = map(lambda x: make_entry(x, query, name), page_content.find_all('li'))
    entries = filter(bool, entries)

    logging.info(f'Scraping {url} done!')

    return list(entries)


options = None

def fill_options():
    website_request = requests.head(f'{domain}/wiki/Category:Responses', timeout=5, allow_redirects=True)
    website_request = requests.get(website_request.url, timeout=5)
    website_content = BeautifulSoup(website_request.content, 'html.parser')
    options = []
    options.append({
        'url': f'{domain}/wiki/Chat_Wheel',
        'name': 'Chat Wheel',
    })
    heroes = list(map(
        lambda a: {
            'url': a['href'],
            'name': ''.join(a.contents).split('/')[0].strip(),
        },
        website_content
            .find(class_='mw-category')
            .find_all('a')
    ))
    heroes.sort(key=lambda hero: len(hero['name']))
    options.extend(heroes)


def scrape(query):
    if options is None:
        fill_options()

    hero_query, *response_query = query.split('/')
    response_query = ''.join(response_query)
    filtered_options = list(filter(
        lambda hero: is_hero_searched(hero_query, hero['name']),
        options,
    ))

    if len(filtered_options) == 0:
        return []

    executor = ThreadPoolExecutor(len(filtered_options))
    results = executor.map(
        lambda hero: collect_sounds(hero, response_query),
        filtered_options,
    )

    return [
        single_result
        for results_list in results
        for single_result in results_list
    ][0:50]
