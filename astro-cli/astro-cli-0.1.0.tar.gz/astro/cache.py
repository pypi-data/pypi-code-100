from pathlib import Path
from diskcache import Cache

cache_path = Path(Path.home() / ".cache" / "astro")
cache = Cache(cache_path)
