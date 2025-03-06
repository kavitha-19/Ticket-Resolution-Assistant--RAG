from vector_search import vector_search
from semantic_ranking import rerank
from graph_query import query_graph_rag

# Define query
query_text = "What are the available payment options for the SaaS project management tool?"

# Step 1: Retrieve top-k documents using vector search
retrieved_docs = vector_search(query_text, top_k=10)
print("results retrieved from vector search/n")
print(retrieved_docs)

print("vector search done")
# Step 2: Re-rank the retrieved results
ranked_docs = rerank(query_text, retrieved_docs)

# Print final ranked results
print("\nTop Ranked Results:")
# for i, ((doc, distance), score) in enumerate(ranked_docs, 1):
#     print(f"{i}. Score: {score:.4f} - {doc[1]}")  # doc[1] contains the document text


for i, ((doc_id, doc_info, doc_text), score) in enumerate(ranked_docs, 1):
    print(f"Rank {i}: Score: {score}")
    print(f"Document ID: {doc_id}")
    print(f"Body: {doc_info.get('Body', '')}")
    print(f"Answer: {doc_info.get('Answer', '')}")
    print("-" * 50)

# Step 3: Query the knowledge graph using GraphRAG
graph_results = query_graph_rag(query_text)

# Print GraphRAG results
print("\nGraphRAG Results:")
for i, doc in enumerate(graph_results, 1):
    print(f"Graph Match {i}:")
    print(f"Subject: {doc.get('subject', 'N/A')}")
    print(f"Body: {doc.get('body', 'N/A')}")
    print(f"Priority: {doc.get('priority', 'N/A')}")
    print(f"Tags: {', '.join(doc.get('tags', []))}")
    print(f"Queue: {doc.get('queue', 'N/A')}")
    print(f"Answer: {doc.get('answer', 'N/A')}")
    print("-" * 50)


# Close DB connection
# close_connection()
