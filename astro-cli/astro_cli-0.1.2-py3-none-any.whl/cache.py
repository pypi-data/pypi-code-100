from pathlib import Path
from diskcache import Cache

CACHE_PATH = Path(Path.home() / ".cache" / "astro")
cache = Cache(CACHE_PATH)
