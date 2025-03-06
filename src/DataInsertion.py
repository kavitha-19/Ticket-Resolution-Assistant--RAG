import os
import json
import psycopg2

# Establish a connection to your PostgreSQL database
conn = psycopg2.connect(
    host="",     # Database Host
    database="",  # Database Name
    user="",      # Username
    password="",  # Password
    port=""           # Port (default for PostgreSQL)
)

# Create a cursor object to interact with the database
cur = conn.cursor()

# Define the path to your folder containing JSON files
folder_path = 'json_docs'

# Loop through each JSON file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        # Open the JSON file and read its content
        with open(os.path.join(folder_path, filename), 'r') as file:
            json_data = json.load(file)

        # Prepare the SQL query to insert data into the tickets table
        insert_query = """
            INSERT INTO tickets (data)
            VALUES (%s);
        """
        
        # Execute the insertion query
        cur.execute(insert_query, (json.dumps(json_data),))

# Commit the transaction to the database
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

print("Data inserted successfully!")
