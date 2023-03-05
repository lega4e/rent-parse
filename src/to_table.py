from src.geo import route_one_to_several
from src.place import CianPlace
from src.utils import orn, tfn


def to_table_row(place: CianPlace, addrs: [str], url: str = None):
  routes = route_one_to_several(' '.join(place.addr), addrs)

  return '\t'.join(map(str, [
    '' if url is None else url,
    ' '.join(place.addr[-2:]),
    orn(lambda: ', '.join(map(lambda u: f'{u.name}\u00a0{u.minutes}\u00a0мин', place.under))),
    orn(lambda: place.price.rent),
    orn(lambda: place.price.commission),
    orn(lambda: place.price.deposit),
    orn(lambda: tfn(place.price.jkh_include, 'Да', 'Нет', None)),
    orn(lambda: place.rooms),
    orn(lambda: place.metres.total),
    orn(lambda: place.metres.habitable),
    orn(lambda: place.metres.kitchen),
    'Да' if 'Кондиционер' in place.items else 'Нет',
    'Да' if 'Посудомоечная машина' in place.items else 'Нет',
    *map(lambda p: p.prettify(), routes)
  ]))

