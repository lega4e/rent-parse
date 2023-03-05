#!python3
import argparse
import sys

from src.cian_pages import get_cian_place, get_cian_links
from src.geo import get_point, get_route
from src.to_table import to_table_row


def make_argparser():
  parser = argparse.ArgumentParser(prog='rentparser',
                                   description='Парсер циана')
  subparsers = parser.add_subparsers(title='Команды')
  
  point = subparsers.add_parser('point')
  point.add_argument('address',
                     type=str,
                     help='Адрес в человековаримом формате')
  point.set_defaults(func=point_command)
  
  route = subparsers.add_parser('route')
  route.add_argument('addr_from',
                     type=str,
                     help='Адрес отправления (в человековаримом формате)')
  route.add_argument('addr_to',
                     type=str,
                     help='Адрес назначения')
  route.set_defaults(func=route_command)
  
  links = subparsers.add_parser('links')
  links.add_argument('url',
                     type=str,
                     help='Страница, откуда следует извлечь ссылки на объявления Циана')
  links.set_defaults(func=links_command)
  
  parse = subparsers.add_parser('parse')
  parse.add_argument('urls',
                     nargs='+',
                     type=str,
                     help='Страницы с предложениями Циана')
  parse.add_argument('--addrs',
                     nargs='+',
                     type=str,
                     default=[],
                     help='Адреса, время и расстояние до которых нужно посчитать')
  parse.set_defaults(func=parse_command)
  return parser


def point_command(args):
  point = get_point(args.address)
  if point is None:
    print(f'Не удалось получить координаты :( попробуйте уточнить адрес')
  else:
    print('%.6f %.6f' % (point.lat, point.lon))


def route_command(args):
  route = get_route(args.addr_from, args.addr_to)
  if route is None:
    print('Не удалось получить маршрут :( попробуйте уточнить адрес')
  else:
    print(route.prettify())
    
    
def links_command(args):
  links = get_cian_links(args.url)
  if links is None:
    print('Что-то пошло не так :(')
  else:
    print(*links, sep='\n')
    
    
def parse_command(args):
  for url in args.urls:
    place = get_cian_place(url)
    if place is None:
      print(f'Со ссылкой {url} что-то пошло не так :(', file=sys.stderr)
    else:
      print(to_table_row(place, addrs=args.addrs, url=url))


def main():
  parser = make_argparser()
  args = parser.parse_args()
  if args.__dict__.get('func') is None:
    parser.print_usage()
    return
  args.func(args)


if __name__ == '__main__':
  main()
