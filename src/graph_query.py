from py2neo import Graph

# Connect to Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "KavithaGraph"))  


# def query_graph_rag(query_text):
#     """
#     Query the knowledge graph to retrieve related tickets based on the input query.
#     """
#     try:
#         cypher_query = """
#         MATCH (t:Ticket)
#         WHERE t.body CONTAINS $query OR t.subject CONTAINS $query
#         RETURN t.id AS ticket_id, t.body AS body, t.subject AS subject, 
#                t.priority AS priority, collect(DISTINCT tag.name) AS tags, 
#                queue.name AS queue, answer.text AS answer
#         LIMIT 5;
#         """
#         results = graph.run(cypher_query, query=query_text).data()
#         print("Graph Query Start")
#         print(results)
#         return results

#     except Exception as e:
#         return f"Error querying Neo4j: {e}"



# def query_graph_rag(query_text):
#     """
#     Query the knowledge graph to retrieve related tickets based on the input query.
#     Now supports multi-word searches by splitting the query into keywords.
#     """
#     try:
#         cypher_query = """
#         WITH split(toLower($query), " ") AS words
#         MATCH (t:Ticket)
#         WHERE ANY(word IN words WHERE toLower(t.body) CONTAINS word OR toLower(t.subject) CONTAINS word)
#         RETURN t.id AS ticket_id, t.body AS body, t.answer AS answer, t.subject AS subject
#         LIMIT 5;
#         """
#         print(f"🔍 Running Query with: '{query_text}'")  # Debugging print
#         results = graph.run(cypher_query, query=query_text.lower()).data()
#         print(f"✅ Query Results: {results if results else 'No matches found'}")
#         return results
 
#     except Exception as e:
#         print(f"❌ Error querying Neo4j: {e}")
#         return []


def query_graph_rag(query_text, top_k=5):  # Add top_k parameter
    """
    Query the knowledge graph to retrieve related tickets based on the input query.
    Now supports multi-word searches by splitting the query into keywords.
    """
    try:
        cypher_query = """
        WITH split(toLower($query), " ") AS words
        MATCH (t:Ticket)
        WHERE ANY(word IN words WHERE toLower(t.body) CONTAINS word OR toLower(t.subject) CONTAINS word)
        RETURN t.id AS ticket_id, t.body AS body, t.answer AS answer, t.subject AS subject
        LIMIT $top_k;  # Use top_k in the query
        """
        print(f"🔍 Running Query with: '{query_text}', Limit: {top_k}")  # Debugging print
        results = graph.run(cypher_query, query=query_text.lower(), top_k=top_k).data()
        print(f"✅ Query Results: {results if results else 'No matches found'}")
        return results
 
    except Exception as e:
        print(f"❌ Error querying Neo4j: {e}")
        return []



#testing ne04j connection
# from py2neo import Graph

# try:
#     graph = Graph("bolt://localhost:7687", auth=("neo4j", "KavithaGraph"))  
#     print("Connected to Neo4j successfully!")
# except Exception as e:
#     print(f"Error connecting to Neo4j: {e}")
