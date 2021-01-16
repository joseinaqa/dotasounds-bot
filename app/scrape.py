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


domain = 'https://dota2.gamepedia.com'

def make_entry(li, query, name):
    source_el = li.find('source')
    title = ''.join(filter(lambda x: not x.name, li.contents)).strip()

    if not source_el or not is_subseq(query, title):
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

    entries = map(lambda x: make_entry(x, query, name), page_content.find_all('li')[0:10])
    entries = filter(bool, entries)

    logging.info(f'Scraping {url} done!')

    return list(entries)[0:5]


website_request = requests.get(f'{domain}/Category:Responses', timeout=5)
website_content = BeautifulSoup(website_request.content, 'html.parser')
heroes = list(map(
    lambda a: {
        'url': a['href'],
        'name': ''.join(a.contents).split('/')[0].strip(),
    },
    website_content
        .find(class_='mw-category')
        .find_all('a')
))
print(heroes)

def scrape(query):
    hero_query, response_query = query.split('/')
    filtered_heroes = list(filter(
        lambda hero: is_hero_searched(hero_query, hero['name']),
        heroes,
    ))[0:10]

    executor = ThreadPoolExecutor(len(filtered_heroes))
    results = executor.map(
        lambda hero: collect_sounds(hero, response_query),
        filtered_heroes,
    )
    return [single_result for results_list in results for single_result in results_list]
