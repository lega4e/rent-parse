import os

from src.lira import Lira


_lira = None

def lira() -> Lira:
  global _lira
  if _lira is None:
    os.makedirs('data', exist_ok=True)
    _lira = Lira('data/data.bin', 'data/head.bin')
  return _lira
