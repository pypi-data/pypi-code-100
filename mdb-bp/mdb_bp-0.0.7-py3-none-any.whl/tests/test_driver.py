import os

from mdb_bp.driver import connect


def test_basic_connect():
    print("")
    print("Username:", os.getenv("DATABASE_USERNAME"))
    print("Password:", os.getenv("DATABASE_PASSWORD"))

    try:
        conn = connect(
            username=os.getenv("DATABASE_USERNAME"),
            password=os.getenv("DATABASE_PASSWORD"),
            connection_protocol="tcp",
            server_address=os.getenv("DATABASE_ADDRESS"),
            server_port=os.getenv("DATABASE_PORT"),
            database_name=os.getenv("DATABASE_NAME"),
            parameters={"interpolateParams": True},
        )
    except Exception as err:
        err = "Err: {}".format(err)
        print(err)
        raise ValueError(err)

    result = conn.exec("USE main")
    print(result)

    print(conn.query("SELECT * FROM sysblockchains"))
    print(conn.query("SELECT * FROM syscolumns"))
    print(conn.query("SELECT * FROM user"))
    conn.close()
