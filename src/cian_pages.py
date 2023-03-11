import os
import re
import time
from typing import Optional

from bs4 import BeautifulSoup
from cloudscraper import create_scraper

from src.parsing import parse_place
from src.place import CianPlace
from src.utils import orn

_dir = 'cian_pages'


def get_cian_links(url: str, pages_num: int) -> [str]:
  try:
    tags = []
    page_num = 1
    while True and page_num <= pages_num:
      page = BeautifulSoup(_create_scraper().get(url).text, 'lxml')
      tags += page.find_all(
        lambda t:
          t.has_attr('href') and
          re.match(r'https://www.cian.ru/rent/flat/\d+/$', t['href'])
      )
      next_page = page.find(
        lambda t:
          t.has_attr('href') and
          re.match(r'https://www\.cian\.ru/cat\.php\?.*?&p=(\d+)&.*', t['href'])
      )
      if next_page is None:
        break
      url = next_page['href']
      page_num += 1
    return [t['href'] for t in tags]
  except Exception as e:
    print(f'Error: {e}')
    return None


def get_cian_place(url: str) -> CianPlace:
  html = _get_local_page(url)
  if html is not None:
    return parse_place(html)
  scraper = _create_scraper()
  html = scraper.get(url).text
  place = parse_place(html)
  if _is_invalid(place):
    time.sleep(5)
    return get_cian_place(url)
  os.makedirs(_dir, exist_ok=True)
  open(_filename(url), 'w').write(html)
  return place


def _is_invalid(place: CianPlace) -> bool:
  return len(place.addr) == 0 or place.rooms is None


def _create_scraper():
  scraper = create_scraper()
  scraper.headers = {'Accept-Language': 'ru'}
  return scraper
  
  
def _filename(url: str) -> str:
  return f'{_dir}/{_translate_url(url)}'


def _get_local_page(url: str) -> Optional[str]:
  return orn(lambda: open(_filename(url), 'r').read())
  
  
def _translate_url(url: str):
  for symbol in '/:&?%@#!$^*()[]{}_+\\|~`\'"':
    url = url.replace(symbol, '_')
  return url
