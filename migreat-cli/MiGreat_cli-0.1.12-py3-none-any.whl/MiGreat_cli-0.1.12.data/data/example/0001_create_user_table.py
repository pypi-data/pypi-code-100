import time

def upgrade(conn):
    conn.execute("""
        CREATE TABLE "user" (
            id BIGSERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            password_hash TEXT NOT NULL
        );

        CREATE UNIQUE INDEX uix_user ON "user" USING BTREE(username);
    """)

    time.sleep(5)

def downgrade(conn):
    """
        DROP TABLE user;
    """
