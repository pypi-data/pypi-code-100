import argparse
import tempfile
from pathlib import Path

import uvicorn

from ruteni import Ruteni, configuration
from ruteni.utils.jwkset import KeyCollection

configuration.set("RUTENI_ENV", "development")

parser = argparse.ArgumentParser()
parser.add_argument(
    "-d",
    "--test-dir",
    type=lambda p: Path(p).absolute(),
    default=Path(tempfile.mkdtemp()).absolute(),
    help="Path to the test directory",
)
parser.add_argument(
    "-s",
    "--static-dir",
    required=False,
    help="Path to the static directory",
)
args = parser.parse_args()

PRIVATE_KEYS = str(args.test_dir / "private_keys.json")
PUBLIC_KEYS = str(args.test_dir / "public_keys.json")
DB_URL = "sqlite:///" + str(args.test_dir / "test.db")

key_collection = KeyCollection(args.test_dir, True)
key_collection.generate()
key_collection.export(PUBLIC_KEYS, PRIVATE_KEYS)

if args.static_dir:
    configuration.set_static_dir(args.static_dir)
else:
    configuration.set_static_dir(Path(__file__).parent / "static")


configuration.set("RUTENI_DATABASE_URL", DB_URL)
configuration.set("RUTENI_SESSION_SECRET_KEY", "secret-key")
configuration.set("RUTENI_JWKEYS_FILE", PRIVATE_KEYS)
configuration.set("RUTENI_VERIFICATION_ABUSE_URL", "<abuse_url>")
configuration.set("RUTENI_VERIFICATION_FROM_ADDRESS", "Accot <contact@accot.fr>")
configuration.set("RUTENI_SITE_NAME", "Ruteni test")

import ruteni.apps.store
import ruteni.plugins.auth.session
import ruteni.plugins.blaze
import ruteni.plugins.logging
import ruteni.plugins.registration
import ruteni.plugins.robots
import ruteni.plugins.security
import ruteni.plugins.socketio

print(DB_URL, sorted(configuration.get_route_paths()))

app = Ruteni()
uvicorn.run(app, host="127.0.0.1", port=8000)
