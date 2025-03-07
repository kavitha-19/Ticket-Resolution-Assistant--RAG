# IT Ticket Resolution Assistant - RAG 

## Overview
The IT Ticket Resolution Assistant is an AI-driven solution that uses a combination of vector search, semantic ranking, and GraphRAG (Retrieve and Generate) to automatically resolve IT tickets. This system integrates multiple models and technologies to provide relevant answers based on historical tickets stored in PostgreSQL and Neo4j.

## Features
- **Vector Search**: Uses Sentence Transformer **all-MiniLM-L6-v2** to find similar tickets based on cosine similarity.
- **Semantic Ranking**: Leverages the **BGE-Reranker-V2m3** model to re-rank retrieved tickets for better relevance.
- **GraphRAG**: Queries a Neo4j Knowledge Graph to find tickets based on relationships and graph-based connections.
- **GPT-4 Integration**: Uses **gpt4o** for natural language chat completion and generating answers.
- **Streamlit UI**: Provides a user-friendly interface for interacting with the AI assistant.

## Architecture

The system consists of the following components:

1. **Frontend (Streamlit)**: The user interacts with the assistant via the Streamlit web interface, where they can query for IT ticket resolutions.
   
2. **Backend (Python Code)**: Python-based backend orchestrating the logic for vector search, semantic reranking, and graph querying.

3. **PostgreSQL Database**: Stores the raw ticket data, including embeddings for the ticket body and answer, allowing efficient retrieval via vector search.

4. **Neo4j Knowledge Graph**: Stores tickets as nodes, linked with relationships (e.g., tags, queue,answers), enabling GraphRAG queries to find related tickets based on contextual information.

5. **AI Services**: 
   - **Vector Search**: Performed using SentenceTransformer's pre-trained model (`all-MiniLM-L6-v2`).
   - **Semantic Ranking**: Performed using BGE-Reranker-V2m3.
   - **GraphRAG**: Uses a combination of graph-based queries and semantic ranking to enhance the ticket resolution process, retrieving contextually relevant data from the knowledge graph (Neo4j).
   - **GPT-4**: Provides chat completions based on the query and context.

## How to Run

### 1. Setup PostgreSQL (here I did through Docker)
- Ensure you have PostgreSQL running locally or in the cloud or through the Docker.
- Create the `tickets` table with columns `id`, `data` (jsonb), `body_embedding`, and `answer_embedding`.
  
    ```
- Once inside PostgreSQL, create the vector extension:
    ```sql
    CREATE EXTENSION vector;
    ```

### 2. Setup Neo4j
- Install Neo4j and run the instance.
- Insert tickets into Neo4j using the provided `graphDataInsertion.py` script.

### 3. Install Dependencies
Install the required Python dependencies:

```bash
pip install -r requirements.txt
