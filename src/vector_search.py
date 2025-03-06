import psycopg2
from sentence_transformers import SentenceTransformer

# Initialize the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Connect to PostgreSQL
# Connect to PostgreSQL Database
conn = psycopg2.connect(
    host="",     # Database Host
    database="",  # Database Name
    user="",      # Username
    password="",  # Password
    port=""           # Port (default for PostgreSQL)
)
cursor = conn.cursor()

# Define the query text
# query_text = "I am reaching out to inquire about the billing cycle and available payment options for the SaaS project management tool. Could you please provide detailed information on the payment plans and any discounts that may be available? I would greatly appreciate it if the information on upgrading or downgrading the plan could also be included?"  # Example query text
query_text = "what are the available payment options for the Saas Project management tool?"
# Generate embedding for the query text
query_embedding = model.encode(query_text).tolist()
# print(query_embedding)
print(len(query_embedding))
# Choose search mode: "body", "answer", or "both"
search_mode = "both"  # Change to "body" or "answer" as needed

if search_mode == "body":
    cursor.execute("""
        SELECT id, data, body_embedding <=> %s::vector AS distance
        FROM tickets
        ORDER BY distance
        LIMIT 10;
    """, (query_embedding,))
elif search_mode == "answer":
    cursor.execute("""
        SELECT id, data, answer_embedding <=> %s::vector AS distance
        FROM tickets
        ORDER BY distance
        LIMIT 10;
    """, (query_embedding,))
elif search_mode == "both":
    cursor.execute("""
        SELECT id, data, 
               (body_embedding <=> %s::vector) AS body_distance,
               (answer_embedding <=> %s::vector) AS answer_distance,
               LEAST(body_embedding <=> %s::vector, answer_embedding <=> %s::vector) AS min_distance
        FROM tickets
        ORDER BY min_distance
        LIMIT 10;
    """, (query_embedding, query_embedding, query_embedding, query_embedding))


# Fetch and print results
results = cursor.fetchall()
for row in results:
    print(f"ID: {row[0]}, Distance: {row[2]}, Data: {row[1]}\n")


# Close connection
cursor.close()
conn.close()
