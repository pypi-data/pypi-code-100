import os

from mdb_bp import driver;


def test_connect():
    conn = driver.connect(
        username=os.getenv("DATABASE_USERNAME"),
        password=os.getenv("DATABASE_PASSWORD"),
        connection_protocol="tcp",
        server_address=os.getenv("DATABASE_ADDRESS"),
        server_port=os.getenv("DATABASE_PORT"),
        database_name=os.getenv("DATABASE_NAME"),
        parameters={"interpolateParams": True},
    )

    try:
        result = conn.exec("USE main")
        print(result)
    except Exception as err:
        print(err)

    # Query from the blockchain
    rows = conn.query("SELECT * FROM user")

    # Print the rows
    itr = iter(rows)

    for row in itr:
        print(row)