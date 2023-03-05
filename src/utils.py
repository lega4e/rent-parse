import sys
import traceback

_print_trackeback_ornone = False

def orn(func, *args, **kwargs):
  try:
    return func(*args, **kwargs)
  except:
    if _print_trackeback_ornone:
      print(traceback.format_exc(), file=sys.stderr)
    return None


def tfn(val: bool, true, false, none):
  return true if val else none if val is None else false
