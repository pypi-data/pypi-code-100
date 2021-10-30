import time

def upgrade(conn):
    conn.execute("""
        ALTER TYPE job ADD VALUE 'pilot';
    """)

    time.sleep(5)

def downgrade(conn):
    """
    """
