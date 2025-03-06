import psycopg2
from psycopg2 import sql

# Connect to PostgreSQL Database
conn = psycopg2.connect(
    host="",     # Database Host
    database="",  # Database Name
    user="",      # Username
    password="",  # Password
    port=""           # Port (default for PostgreSQL)
)

# Create a cursor object to interact with the database
cur = conn.cursor()

# Create a Sequence (Optional: If you want to set custom starting point)
cur.execute("""
    CREATE SEQUENCE ticket_id_seq
    START WITH 101;
""")

# Create the Tickets Table
cur.execute("""
    CREATE TABLE tickets (
        id INT DEFAULT nextval('ticket_id_seq') PRIMARY KEY,
        data JSONB NOT NULL
    );
""")

conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

print("Table created successfully!")
