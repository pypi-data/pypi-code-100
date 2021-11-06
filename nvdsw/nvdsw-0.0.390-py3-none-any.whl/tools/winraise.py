import Xlib
from ewmh import EWMH
import logging

log = logging.getLogger('winraise')

ewmh = EWMH()

def winraise(window_name):
# this function is scheduled via the GTK loop
# so the return codes are false if the operation is done done (as in, do NOT REPEAT) ir true (please keep trying)

  wins = ewmh.getClientList()
  for w in wins:
    wname = None
    try:
      wname = w.get_wm_name()
    except Xlib.error.BadWindow:
      continue

    if wname is None:
      continue

#     print("wname: " + wname)
    if wname == window_name:
      ewmh.setActiveWindow(w)
#       print('Window raised')
      wtop = ewmh.getActiveWindow()
      if wtop == w: 
        log.debug("window to raise: " + window_name + " was raised and the operation took effect")
        return False
      else:
#         print("raised window but the operation did not go through")
        log.debug("window to raise: " + window_name + " was raised but the operation did not take effect")
        return True
 
#   print("window to raise not found")
  log.debug("window to raise: " + window_name + " was not found")
  return True