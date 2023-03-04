import json
import re

import requests

import src.translate as tr

from bs4 import BeautifulSoup
from typing import Optional

from src.lira_di import lira


class GeoPoint:
  def __init__(self, lat: float, lon: float):
    self.lat = lat
    self.lon = lon

  def __str__(self):
    return f'<GeoPoint {self.__dict__}>'

  def __repr__(self):
    return self.__str__()


class Route:
  def __init__(self, minutes: int, metres: int):
    self.minutes = minutes
    self.metres = metres

  def __str__(self):
    return f'<Route {self.__dict__}>'

  def __repr__(self):
    return self.__str__()

  def prettify(self):
    metres = (f' {(self.metres / 1000)}\u00a0км'
          if self.metres is not None else
          '')
    return f'{self.minutes}\u00a0мин{metres}'


# get point funcitons
def get_point(addr: str) -> Optional[GeoPoint]:
  """
  По адресу получает координаты
  :param addr: Адрес записаный по-человечески
  :return: Координаты (если не получается, то None)
  """
  addr = addr[:addr.rfind('/')]
  if lira().get(addr) is not None:
    return lira().get(addr) or None
  data = json.loads(requests.get(_make_geocoder_url(addr)).text)
  members = data['response']['GeoObjectCollection']['featureMember']
  if len(members) == 0:
    lira().put(False, id=addr)
    lira().flush()
    return None
  pos = members[0]['GeoObject']['Point']['pos']
  m = re.match(r'(\d+\.\d+)\D+(\d+\.\d+)', pos)
  geo = GeoPoint(lat=m.group(2), lon=m.group(1))
  lira().put(geo, id=addr)
  lira().flush()
  return geo


# get route runctions
def get_route(addr_from: str, addr_to: str) -> Route:
  """
  Возвращает количество минут пешком и метров от одной точки до другой
  :param addr_from: Адрес откуда (по-человечески)
  :param addr_to: Адрес куда (по-человечески)
  :return: минуты и метры
  """
  return get_route_p(get_point(addr_from), get_point(addr_to))


def get_route_p(a: GeoPoint, b: GeoPoint) -> Route:
  """
  Возвращает количество минут пешком и метров от одной точки до другой
  """
  html = requests.get(_make_minutes_url(
    ll=f'{a.lon}+{a.lat}',
    rtext=f'{a.lat}+{a.lon}~{b.lat}+{b.lon}',
  )).text
  soup = BeautifulSoup(html, 'lxml')
  div = soup.find(class_='pedestrian-route-snippet-view__route-title-primary')
  return Route(
    minutes=_parse_minutes(div.text),
    metres=_parse_metres(div.next_sibling.text)
  )


def route_one_to_several(one: str, several: [str]) -> [Route]:
  return route_one_to_several_p(
    get_point(one),
    [p for p in [get_point(p) for p in several] if p is not None]
  )


def route_one_to_several_p(one: GeoPoint, several: [GeoPoint]) -> [Route]:
  return [get_route_p(one, point_to) for point_to in several]


# parse functions
def _parse_minutes(text: str) -> int:
  """
  Извлекает из строки значение о времени, переводит в минуты.
  Формат строки: "1 ч 33" мин или "2 ч" или "30 мин" или "1 дн. 3 ч"
  :param text: Строка по формату
  :return: Количество минут
  """
  m = re.match(r'((\d+)\D+дн\.\D*)?((\d+)\D+ч\D*)?((\d+)\D+мин\D*)?', text)
  minutes = 0
  if m.group(2) is not None:
    minutes += int(m.group(2)) * 86400
  if m.group(4) is not None:
    minutes += int(m.group(4)) * 60
  if m.group(6) is not None:
    minutes += int(m.group(6))
  return minutes


def _parse_metres(text: str) -> int:
  """
  Извлекает из строки информацию о расстоянии, возвращает в метрах.
  Формат строки: "1 км" или "1,43 км" или "340 м"
  :param text:
  :return:
  """
  if 'км' in text:
    m = re.match(r'(\d+)(,(\d+))?', text)
    metres = m.group(1)
    if m.group(3) is not None:
      metres += '.' + m.group(3)
    return int(float(metres) * 1000)
  else:
    return tr.integer(text)


# make url functions
def _make_geocoder_url(
    geocode: str,
    apikey: str = '3c7d784f-3421-445c-be2b-bdc5b41c59e4',
    format: str = 'json',
    url: str = 'https://geocode-maps.yandex.ru/1.x',
):
  return _make_url(url, geocode=geocode, apikey=apikey, format=format)


def _make_minutes_url(
    rtext: str,
    url: str = 'https://yandex.ru/maps',
    ll: str = '37.580119%2C55.742154',
    mode: str = 'routes',
    rtt: str = 'pd',
):
  return _make_url(
    url=url,
    ll=ll,
    mode=mode,
    rtext=rtext,
    rtt=rtt,
  )


def _make_url(url, **options):
  options_string = ''
  if len(options) > 0:
    options_string = ('?' + '&'.join(f'{key}={value}'
                     for key, value
                     in options.items()
                     if value is not None))
  return f'{url}' + options_string

