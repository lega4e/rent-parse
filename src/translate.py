import re


def rooms(title: str) -> int:
  return int(re.match(r'\s*(\d+)-', title).group(1))


def integer(text: str) -> int:
  return int(''.join(filter(lambda x: x.isdigit(), text)))


def floating(text: str) -> float:
  text = ''.join(filter(lambda s: s.isdigit() or s == ',', text))
  return float(text.replace(',', '.'))


def floor(text: str) -> (int, int):
  m = re.match(r'(\d+)\D+(\d+)', text)
  return int(m.group(1)), int(m.group(2))
