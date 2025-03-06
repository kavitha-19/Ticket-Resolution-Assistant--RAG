# from sentence_transformers import CrossEncoder
# import torch

# # Load the reranker model and move it to GPU if available
# device = "cuda" if torch.cuda.is_available() else "cpu"
# # Path to the downloaded model directory
# local_model_path = "C:/Users/Kavitha padala/Desktop/ICM_RAG/models/bge-reranker-v2m3"
# reranker = CrossEncoder(local_model_path, device=device)


# def rerank(query, retrieved_docs):
#     """Re-rank the retrieved documents using the selected model."""
#     try:
#         # Ensure retrieved_docs contains (id, text) tuples

#         doc_texts = [row[1] if isinstance(row, (list, tuple)) and len(row) > 1 else str(row) for row in retrieved_docs]

#         # Create query-document pairs
#         pairs = [(query, doc) for doc in doc_texts]  

#         # Get relevance scores
#         scores = reranker.predict(pairs)

#         # Sort documents based on scores (higher score = more relevant)
#         ranked_results = sorted(zip(retrieved_docs, scores), key=lambda x: x[1], reverse=True)
        
#         print("Results from semantic ranking:")
#         print(ranked_results)
#         return ranked_results

#     except Exception as e:
#         print(f"Error during reranking: {e}")
#         return retrieved_docs  # Return original docs if an error occurs


from sentence_transformers import CrossEncoder
import torch

# Load the reranker model and move it to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
# Path to the downloaded model directory
local_model_path = "C:/Users/Kavitha padala/Desktop/ICM_RAG/models/bge-reranker-v2m3"
reranker = CrossEncoder(local_model_path, device=device)

def rerank(query, retrieved_docs):
    """Re-rank the retrieved documents using the selected model."""
    try:
        doc_texts = []
        cleaned_docs = []

        for row in retrieved_docs:
            if isinstance(row, (tuple, list)) and len(row) >= 2 and isinstance(row[1], dict):
                doc_id, doc_info = row[0], row[1]  # Extract ID and dictionary
                # Combine Body and Answer for better ranking
                doc_text = doc_info.get("Body", "").strip() + " " + doc_info.get("Answer", "").strip()
            else:
                doc_id, doc_text = None, str(row)  # Fallback case

            doc_texts.append(doc_text)
            cleaned_docs.append((doc_id, doc_info, doc_text))  # Keep original info

        # Create query-document pairs
        pairs = [(query, doc) for doc in doc_texts]

        # Get relevance scores
        scores = reranker.predict(pairs)

        # Sort documents based on scores (higher score = more relevant)
        ranked_results = sorted(zip(cleaned_docs, scores), key=lambda x: x[1], reverse=True)

        print("\nResults from Semantic Ranking:")
        return ranked_results

    except Exception as e:
        print(f"Error during reranking: {e}")
        return retrieved_docs  # Return original docs if an error occurs



