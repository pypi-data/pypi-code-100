from mdb_bp.config import config
from mdb_bp.utils import bytes_to_string


def test_basic_interpolate():
    basic_cfg = config()

    salt, pw_hash = basic_cfg.hash_password("I like to test")

    # Initialize test cases
    test_cases = [
        {
            "query": "INSERT main.user (first_name, last_name, age) VALUES (?, ?, ?)",
            "params": ["John", "Smith", 20],
            "exp": "INSERT main.user (first_name, last_name, age) VALUES (\"John\", \"Smith\", 20)"
        },
        {
            "query": "SELECT * FROM main.user WHERE user.name <> ? AND user.age > ?",
            "params": ["john", 21],
            "exp": "SELECT * FROM main.user WHERE user.name <> \"john\" AND user.age > 21"
        },
        {
            "query": "DISCONTINUE main.user (id) VALUES (?)",
            "params": [847935],
            "exp": "DISCONTINUE main.user (id) VALUES (847935)"
        },
        {
            "query": "INSERT main.user (stripe_id, first_name, last_name, email, phone_number, password_hash, salt) VALUES (?, ?, ?, ?, ?, ?, ?) OUTPUT id",
            "params": [
                "J3V60cVnmGcvM3",
                "John", "Smith",
                "john@smith.com", "+1 (123) 456-7788",
                pw_hash, salt,
            ],
            "exp": 'INSERT main.user (stripe_id, first_name, last_name, email, phone_number, password_hash, salt) VALUES ("J3V60cVnmGcvM3", "John", "Smith", "john@smith.com", "+1 (123) 456-7788", {}, {}) OUTPUT id'.format(
                bytes_to_string(pw_hash), bytes_to_string(salt))
        }
    ]

    # Run through all of the cases
    for case in test_cases:
        query = case["query"]
        params = case["params"]
        exp_resp = case["exp"]

        resp = basic_cfg.interpolate_params(query, params)
        if resp != exp_resp:
            raise ValueError("interpolate_params() resp = {}, want = {}".format(resp, exp_resp))


def test_basic_password_hash():
    basic_cfg = config()

    salt, pw_hash = basic_cfg.hash_password("meow")
    print("Salt: {}".format(salt))
    print("Encoded Salt: {}".format(bytes_to_string(salt)))
    print("Password Hash: {}".format(pw_hash))
    print("Encoded Password Hash: {}".format(bytes_to_string(pw_hash)))
