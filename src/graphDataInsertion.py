import os
import json
from py2neo import Graph, Node, Relationship

# Connect to Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "KavithaGraph"))  

# Path to your JSON files folder
json_folder = "C:/Users/Kavitha padala/Desktop/ICM_RAG/json_docs"

# Function to insert a ticket into Neo4j
def insert_ticket_into_neo4j(ticket_data):
    # Create Ticket node
    ticket = Node(
        "Ticket",
        id=ticket_data["ID"],
        body=ticket_data["Body"],
        type=ticket_data["Type"],
        subject=ticket_data["Subject"],
        language=ticket_data["Language"],
        priority=ticket_data["Priority"]
    )
    graph.merge(ticket, "Ticket", "id")

    # Create & link Tags
    for tag_name in ticket_data.get("Tags", []):
        tag = Node("Tag", name=tag_name)
        graph.merge(tag, "Tag", "name")
        graph.merge(Relationship(ticket, "HAS_TAG", tag))

    # Create & link Queue
    queue_name = ticket_data.get("Queue", "Unknown")
    queue = Node("Queue", name=queue_name)
    graph.merge(queue, "Queue", "name")
    graph.merge(Relationship(ticket, "BELONGS_TO", queue))

    # Create & link Answer
    if ticket_data.get("Answer"):
        answer = Node("Answer", text=ticket_data["Answer"])
        graph.create(answer)
        graph.create(Relationship(ticket, "HAS_ANSWER", answer))

# Loop through all JSON files in the folder
for filename in os.listdir(json_folder):
    if filename.endswith(".json"):  
        file_path = os.path.join(json_folder, filename)
        
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                ticket_data = json.load(file)  # Load JSON data
                insert_ticket_into_neo4j(ticket_data)  # Insert into Neo4j
                print(f"Inserted: {filename}")
            except json.JSONDecodeError as e:
                print(f"Error parsing {filename}: {e}")

print("✅ All JSON files inserted successfully into Neo4j!")
