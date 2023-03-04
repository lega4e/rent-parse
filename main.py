#!python3

import sys

from cloudscraper import create_scraper

from src.cian_pages import get_cian_place, get_cian_links
from src.parsing import parse_place
from src.place import CianPlace
from src.geo import get_point, get_route
from src.to_table import to_table_row

urls_global = [
  'https://www.cian.ru/rent/flat/283105175/',
  'https://www.cian.ru/rent/flat/283907495/',
  'https://www.cian.ru/rent/flat/240400774/',
  'https://www.cian.ru/rent/flat/280696517/',
  'https://www.cian.ru/rent/flat/283635661/',
  'https://www.cian.ru/rent/flat/283499711/',
  'https://www.cian.ru/rent/flat/279331094/',
  'https://www.cian.ru/rent/flat/283723910/',
  'https://www.cian.ru/rent/flat/279767038/',
  'https://www.cian.ru/rent/flat/283324821/',
  'https://www.cian.ru/rent/flat/284167193/',
  'https://www.cian.ru/rent/flat/284224599/',
  'https://www.cian.ru/rent/flat/283531186/',
  'https://www.cian.ru/rent/flat/281472489/',
  'https://www.cian.ru/rent/flat/280638784/',
  'https://www.cian.ru/rent/flat/282153921/',
]

urls_global2 = [
  'https://www.cian.ru/rent/flat/284433144/',
  'https://www.cian.ru/rent/flat/283629140/',
  'https://www.cian.ru/rent/flat/284375779/',
  'https://www.cian.ru/rent/flat/272766324/',
  'https://www.cian.ru/rent/flat/284082701/',
  'https://www.cian.ru/rent/flat/266606647/',
  'https://www.cian.ru/rent/flat/280753983/',
  'https://www.cian.ru/rent/flat/279427093/',
  'https://www.cian.ru/rent/flat/283622552/',
  'https://www.cian.ru/rent/flat/284207614/',
  'https://www.cian.ru/rent/flat/282452518/',
  'https://www.cian.ru/rent/flat/248164188/',
  'https://www.cian.ru/rent/flat/283813056/',
  'https://www.cian.ru/rent/flat/196343481/',
  'https://www.cian.ru/rent/flat/284420738/',
  'https://www.cian.ru/rent/flat/282092792/',
  'https://www.cian.ru/rent/flat/278802162/',
  'https://www.cian.ru/rent/flat/283855871/',
  'https://www.cian.ru/rent/flat/279705148/',
  'https://www.cian.ru/rent/flat/279799496/',
  'https://www.cian.ru/rent/flat/281809683/',
  'https://www.cian.ru/rent/flat/282047026/',
  'https://www.cian.ru/rent/flat/284234424/',
  'https://www.cian.ru/rent/flat/284236441/',
  'https://www.cian.ru/rent/flat/284188129/',
  'https://www.cian.ru/rent/flat/284196586/',
  'https://www.cian.ru/rent/flat/281354449/',
  'https://www.cian.ru/rent/flat/283966491/',
]

addrs_global = [
  ('Плотников переулок 10', 'Новинский бул., 8, Москва'),
  ('Плотников переулок 10', 'ул. Льва Толстого, 16, Москва'),
  ('Плотников переулок 10', 'Староконюшенный переулок, 5/14'),
  ('1-я улица Машиностроения, 4к2', 'Староконюшенный переулок, 5/14'),
]



def point_test():
  a = addrs_global[0][0]
  b = addrs_global[0][1]
  for addr in [a, a, b]:
    print(addr, '->', get_point(addr))
    
    
def get_cian_links_test():
  url = 'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&foot_min=45&maxprice=80000&metro%5B0%5D=56&metro%5B1%5D=86&metro%5B2%5D=115&offer_type=flat&only_foot=2&room1=1&type=4'
  links = get_cian_links(url)
  print(*links, sep='\n')


def cian_urls_test():
  addrs = [
    # 'Плотников переулок 10',
    # 'Староконюшенный переулок, 5/14',
    # 'Новинский бул., 8, Москва',
    # 'ул. Льва Толстого, 16, Москва',
  ]
  for url in urls_global2:
    place = get_cian_place(url)
    print(to_table_row(place, addrs=addrs, url=url))


def geo_test():
  for addr_from, addr_to in addrs_global:
    print(addr_from, '->', addr_to)
    route = get_route(addr_from, addr_to)
    print(route.minutes, 'минут', route.metres, 'метров')
    print()


def print_cian(cian: CianPlace):
  print(cian.__dict__)


def cian_test():
  if len(sys.argv) >= 2:
    scraper = create_scraper()
    scraper.headers = {'Accept-Language': 'ru'}
    html = scraper.get(url=sys.argv[1]).text
    if len(sys.argv) >= 3:
      with open('out3.html', 'w') as file:
        file.write(html)
    place = parse_place(html)
  else:
    place = parse_place(open('out2.html').read())
  print(place)
  lon, lat = get_point(' '.join(place.addr))
  print(lon, lat)


def main():
  cian_urls_test()


if __name__ == '__main__':
  main()
