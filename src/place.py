class Underground:
  def __init__(
    self,
    name: str = None,
    minutes: int = None,
  ):
    self.name = name
    self.minutes = minutes

  def __str__(self):
    return (f'<Underground name: {self.name}, '
            + f'minutes: {self.minutes}>')

  def __repr__(self):
    return self.__str__()


class Metres:
  def __init__(
    self,
    total: float = None,
    kitchen: float = None,
    habitable: float = None,
  ):
    self.total = total
    self.kitchen = kitchen
    self.habitable = habitable

  def __str__(self):
    return (f'<Metres total: {self.total}, '
            + f'kitchen: {self.kitchen}, '
            + f'habitable: {self.habitable}>')

  def __repr__(self):
    return self.__str__()


class Price:
  def __init__(
      self,
      rent: int = None,
      commission: int = None,
      deposit: int = None,
  ):
    self.rent = rent
    self.commission = commission
    self.deposit = deposit

  def __str__(self):
    return (f'<Price rent: {self.rent}, '
            + f'commission: {self.commission}, '
            + f'deposit: {self.deposit}>')

  def __repr__(self):
    return self.__str__()


class Floor:
  def __init__(
    self,
    total: int = None,
    current: int = None,
  ):
    self.total = total
    self.current = current

  def __str__(self):
    return (f'<Floor total: {self.total}, '
            + f'current: {self.current}>')

  def __repr__(self):
    return self.__str__()


class CianPlace:
  def __init__(
    self,
    price: Price = None,
    rooms: int = None,
    addr: [str] = None,
    metres: Metres = None,
    under: [Underground] = None,
    floor: Floor = None,
    description: str = None,
    params: {str: str} = None,
    items: [str] = None
  ):
    self.price = price
    self.rooms = rooms
    self.addr = addr
    self.metres = metres
    self.under = under
    self.floor = floor
    self.description = description
    self.params = params
    self.items = items

  def __str__(self):
    return (f'<CianPlace\n'
            + f'  price:  {self.price},\n'
            + f'  rooms:  {self.rooms},\n'
            + f'  addr:   {self.addr},\n'
            + f'  metres: {self.metres},\n'
            + f'  under:  {self.under},\n'
            + f'  floor:  {self.floor},\n'
            + f'  params: {self.params},\n'
            + f'  items:  {self.items}>')

  def __repr__(self):
    return self.__str__()
