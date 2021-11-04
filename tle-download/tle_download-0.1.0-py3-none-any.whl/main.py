import sys
import time
import urllib.parse

from enum import Enum
from pathlib import Path
from typing import List

import httpx
import typer


class SearchType(str, Enum):
  line0 = "line0"
  catid = "catid"


def get_tles(username, password, stype, searches, sleep=3):
  url = "https://www.space-track.org/basicspacedata/query/class/tle_latest/ORDINAL/1/TLE_LINE0/~~{}/DECAYED/<>1/orderby/ORDINAL%20desc/format/3le/"

  if stype == 'catid':
    url = "https://www.space-track.org/basicspacedata/query/class/tle_latest/ORDINAL/1/NORAD_CAT_ID/{}/orderby/ORDINAL%20desc/format/3le/"

  client = httpx.Client()
  client.post(
    "https://www.space-track.org/ajaxauth/login",
    data={
      'identity': username,
      'password': password,
    }
  )

  ret = []
  for i, search in enumerate(searches):
    search_url = url.format(urllib.parse.quote(search))
    typer.echo(f'Getting: {search_url}')
    response = client.get(search_url)
    if response.status_code != 200:
      typer.secho(f'Error: {response.status_code}')

    lines = response.text.strip().splitlines()
    for i, line in enumerate(lines):
      if line.startswith('0 ') and not line.endswith(' DEB'):
        line = line[2:]
        tle_lines = [line, lines[i + 1], lines[i + 2]]
        ret.append(tle_lines)

    if i != len(searches) - 1:
      time.sleep(3)

  return ret


def write_tles(outpath, tles):
  with outpath.open('w') as fh:
    for tle in tles:
      fh.write("\n".join(tle))
      fh.write("\n")


def run(
  search_type: SearchType,
  searches: List[str],
  username: str = typer.Option(None, envvar="SPACE_TRACK_USERNAME"),
  password: str = typer.Option(None, envvar="SPACE_TRACK_PASSWORD"),
  outpath: Path = typer.Option('tles.txt', file_okay=True, dir_okay=False, writable=True),
  sleep: int = typer.Option(3, help="sleep between requests so you don't break API limits"),
):
  if username is None or password is None:
    typer.secho("Space Track username and password are required.", fg=typer.colors.RED)
    sys.exit(1)

  tles = get_tles(username, password, search_type.value, searches, sleep=sleep)
  write_tles(outpath, tles)


def cli():
  typer.run(run)


if __name__ == "__main__":
  cli()
