import logging
import sys

# configurando logging
log = logging.getLogger("manga_scrap")
log.setLevel(logging.DEBUG)
format = logging.Formatter("[%(name)s][%(levelname)s][%(asctime)s]: %(message)s")
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
log.addHandler(ch)