import traceback

_print_trackeback_ornone = False

def orn(func, *args, **kwargs):
  try:
    return func(*args, **kwargs)
  except:
    if _print_trackeback_ornone:
      print(traceback.format_exc())
    return None
