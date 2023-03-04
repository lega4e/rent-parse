import traceback

import src.translate as tr

from bs4 import BeautifulSoup, Tag
from copy import deepcopy
from typing import Optional

from src.place import *

_print_trackeback_ornone = False


class TagValue:
  def __init__(self, tag: str, value: str):
    self.tag = tag
    self.value = value

  def __call__(self, tag: Tag) -> bool:
    return (tag.has_attr(self.tag)
        and tag.attrs[self.tag] == self.value)


def parse_place(html: str) -> CianPlace:
  soup = BeautifulSoup(html, 'lxml')
  params = orn(get_params, soup)
  return CianPlace(
    price=orn(get_price, soup),
    rooms=orn(tr.rooms, orn(get_title, soup)),
    addr=orn(get_addr, soup),
    metres=orn(metres_from_params, params),
    under=orn(get_under, soup),
    description=orn(get_desc, soup),
    floor=orn(get_floor, soup),
    params=orn(remove_metres_params, params),
    items=orn(get_items, soup),
  )


def get_title(soup: BeautifulSoup) -> Optional[str]:
  return data_tags(soup, 'OfferTitleNew')[0].text


def get_price(soup: BeautifulSoup) -> Price:
  tags = data_tags(soup, 'OfferFactItem')
  items = {}
  for tag in tags:
    items[tag.p.text] = orn(
      lambda: tag.p.next_sibling.next_sibling.text)
  items['Цена'] = orn(
    lambda: data_tags(soup, 'PriceInfo')[0].div.span.text)
  price = Price()
  price.rent = orn(tr.integer, items.get('Цена'))
  price.deposit = orn(tr.integer, items.get('Залог'))
  if price.deposit is None and items.get('Предоплата') == '1 месяц':
    price.deposit = price.rent
  if items.get('Комиссии') is not None and 'нет' in items['Комиссии']:
    price.commission = 0
  else:
    price.commission = orn(tr.integer, items.get('Комиссия'))
  return price


def get_addr(soup: BeautifulSoup) -> [str]:
  return list(map(lambda tag: tag.text, data_tags(soup, 'AddressItem')))


def get_under(soup: BeautifulSoup) -> [str]:
  return [Underground(name=tag.a.text, minutes=orn(tr.integer, tag.span.text))
      for tag
      in data_tags(soup, 'UndergroundItem')]


def get_params(soup: BeautifulSoup) -> [str]:
  names = [
    'Общая площадь',
    'Жилая площадь',
    'Площадь кухни',
    'Санузел',
    'Балкон/лоджия',
    'Вид из окон',
    'Можно с детьми',
    'Можно с животными',
  ]
  div = data_tags(soup, 'OfferSummaryInfoGroup')[0]
  res = {}
  for name in names:
    tag = div.find(lambda t: t.text.strip() == name)
    if tag is not None:
      res[name] = tag.next_sibling.text
  return res


def get_items(soup: BeautifulSoup) -> [str]:
  return list(map(lambda tag: tag.text, data_tags(soup, 'FeaturesItem')))


def get_desc(soup: BeautifulSoup) -> [str]:
  return soup.find(id='description').text


def get_floor(soup: BeautifulSoup) -> Floor:
  text = soup.find(lambda t: t.text.strip() == 'Этаж').next_sibling.text
  current, total = tr.floor(text)
  return Floor(current=current, total=total)


def metres_from_params(params: {str: str}) -> Metres:
  return Metres(
    total=orn(tr.floating, params['Общая площадь']),
    habitable=orn(tr.floating, params['Жилая площадь']),
    kitchen=orn(tr.floating, params['Площадь кухни']),
  )


def remove_metres_params(params: {str: str}) -> {str: str}:
  params = deepcopy(params)
  for param in ['Общая площадь', 'Жилая площадь', 'Площадь кухни']:
    if params.get(param) is not None:
      del params[param]
  return params


def data_tags(soup: BeautifulSoup, value: str) -> [Tag]:
  return list(soup.find_all(TagValue('data-name', value)))


def orn(func, *args, **kwargs):
  try:
    return func(*args, **kwargs)
  except:
    if _print_trackeback_ornone:
      print(traceback.format_exc())
    return None
