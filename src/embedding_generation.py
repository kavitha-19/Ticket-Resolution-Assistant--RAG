# from sentence_transformers import SentenceTransformer
# import psycopg2
# import numpy as np

# # Initialize the SentenceTransformer model
# model = SentenceTransformer('all-MiniLM-L6-v2')

# conn = psycopg2.connect(
#     host="127.0.0.1",     # Database Host
#     database="postgres",  # Database Name
#     user="postgres",      # Username
#     password="postgres",  # Password
#     port="5432"           # Port (default for PostgreSQL)
# )
# cursor = conn.cursor()

# # Step 1: Install the pgvector extension if it's not already installed
# cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
# conn.commit()

# # Step 2: Add the 'embedding' column if it doesn't exist
# cursor.execute("""
#     ALTER TABLE tickets
#     ADD COLUMN IF NOT EXISTS embedding vector(768);  -- 768 is the size of your combined embeddings
# """)
# conn.commit()

# # Fetch all tickets data from the tickets table
# cursor.execute("SELECT id, data FROM tickets")  # Replace jsonb_column with your actual column name containing the JSONB data
# tickets = cursor.fetchall()

# # Loop through tickets, generate embeddings for Body and Answer and update embeddings in the database
# for ticket in tickets:
#     ticket_id, json_data = ticket  # Ticket ID and JSON data
#     body = json_data['Body']  # Extract Body field from JSON
#     answer = json_data['Answer']  # Extract Answer field from JSON
    
#     # Generate embeddings for Body and Answer
#     body_embedding = model.encode(body)
#     answer_embedding = model.encode(answer)
    
#     # Combine the embeddings (concatenate the two vectors)
#     combined_embedding = np.concatenate((body_embedding, answer_embedding), axis=0)

#     # Check the size of the combined embedding
#     embedding_size = len(combined_embedding)
#     # print(f"Embedding size: {embedding_size}")
    
#     # Convert numpy array to a list for PostgreSQL insertion
#     embedding_list = combined_embedding.tolist()

#     # Update the ticket's embedding column
#     cursor.execute("""
#         UPDATE tickets
#         SET embedding = %s
#         WHERE id = %s
#     """, (embedding_list, ticket_id))

# # Commit changes and close the connection
# conn.commit()
# cursor.close()
# conn.close()

# print("Embeddings updated successfully for all tickets!")


from sentence_transformers import SentenceTransformer
import psycopg2
import numpy as np

# Initialize the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="127.0.0.1",     # Database Host
    database="postgres",  # Database Name
    user="postgres",      # Username
    password="postgres",  # Password
    port="5432"           # Port (default for PostgreSQL)
)
cursor = conn.cursor()

# Step 1: Install the pgvector extension if it's not already installed
cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
conn.commit()

# Step 2: Add 'body_embedding' and 'answer_embedding' columns if they don't exist
cursor.execute("""
    ALTER TABLE tickets
    ADD COLUMN IF NOT EXISTS body_embedding vector(384),
    ADD COLUMN IF NOT EXISTS answer_embedding vector(384);
""")
conn.commit()

# Fetch all tickets data from the tickets table
cursor.execute("SELECT id, data FROM tickets")  # 'data' contains the JSONB column
tickets = cursor.fetchall()

# Loop through tickets, generate embeddings for Body and Answer, and update the database
for ticket in tickets:
    ticket_id, json_data = ticket  # Ticket ID and JSON data
    
    body = json_data.get('Body', '')  # Extract Body field from JSON, default to empty string if missing
    answer = json_data.get('Answer', '')  # Extract Answer field from JSON, default to empty string if missing
    
    # Generate separate embeddings
    body_embedding = model.encode(body).tolist()  # 384-dimensional
    answer_embedding = model.encode(answer).tolist()  # 384-dimensional

    # Update the ticket's body_embedding and answer_embedding columns
    cursor.execute("""
        UPDATE tickets
        SET body_embedding = %s, answer_embedding = %s
        WHERE id = %s
    """, (body_embedding, answer_embedding, ticket_id))

# Commit changes and close the connection
conn.commit()
cursor.close()
conn.close()

print("Embeddings updated successfully for all tickets!")

