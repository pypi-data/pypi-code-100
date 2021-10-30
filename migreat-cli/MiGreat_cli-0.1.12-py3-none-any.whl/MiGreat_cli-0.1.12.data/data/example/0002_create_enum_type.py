import time

def upgrade(conn):
    conn.execute("""
        CREATE TYPE job AS ENUM (
            'programmer',
            'bus driver',
            'doctor',
            'teacher'
        );
    """)

    time.sleep(5)

def downgrade(conn):
    """
        DROP TYPE job;
    """
