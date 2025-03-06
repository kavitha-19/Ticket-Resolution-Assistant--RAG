

# import streamlit as st
# import requests
# import json

# # Streamlit UI setup
# st.set_page_config(page_title="Ticket Resolution Assistant", layout="wide")
# st.title("🎫 Ticket Resolution Assistant")
# st.markdown("Chat with the AI Assistant for ICM Ticket Resolution.")

# # Sidebar for model selection
# with st.sidebar:
#     st.header("⚙️ Configuration")
#     model_type = st.selectbox("Select Model Type:", ["Vector", "Semantic", "GraphRAG"])
    

# # Load chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Load chat history from a JSON file
# chat_history_file = "chat_history.json"
# try:
#     with open(chat_history_file, "r") as file:
#         st.session_state.messages = json.load(file)
# except FileNotFoundError:
#     st.session_state.messages = []

# # Display chat history
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # User input
# user_input = st.chat_input("Type your question here...")

# if user_input:
#     # Display user message
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     with st.chat_message("user"):
#         st.markdown(user_input)

#     # API request
#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):
#             try:
#                 response = requests.post(api_url, json={"model": model_type, "query": user_input})
#                 if response.status_code == 200:
#                     answer = response.json().get("answer", "No answer found.")
#                 else:
#                     answer = f"Error: {response.status_code} - {response.text}"
#             except Exception as e:
#                 answer = f"Failed to connect to the API. Error: {str(e)}"

#             st.markdown(answer)
#             st.session_state.messages.append({"role": "assistant", "content": answer})

#     # Save chat history to a JSON file
#     with open(chat_history_file, "w") as file:
#         json.dump(st.session_state.messages, file)





 
import streamlit as st
import json
import os
import sys
from src.vector_search import vector_search
from src.semantic_ranking import rerank
# from testing import chat_completion
from chat import initialize_services
from src.graph_query import query_graph_rag
# import streamlit as st






# Streamlit UI setup

service = initialize_services()



st.set_page_config(page_title="IT Ticket Resolution Assistant", layout="wide")
st.title("🎫 IT Ticket Resolution Assistant")
st.markdown("Chat with the AI Assistant for IT Ticket Resolution.")

# Sidebar for model selection
with st.sidebar:
    logo_path = "logo.png"  # Ensure your logo file is in the same directory
    st.sidebar.image(logo_path, use_container_width=True)
    # st.header("⚙️ Settings")
    model_type = st.selectbox("Select Model Type:", ["Vector", "Semantic", "GraphRAG"])


# Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []  # Reset chat history
        with open("chat_history.json", "w") as file:
            json.dump([], file)  # Clear saved history
        st.rerun()  # Refresh the UI

# Load chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Load chat history from a JSON file
chat_history_file = "chat_history.json"
try:
    with open(chat_history_file, "r") as file:
        st.session_state.messages = json.load(file)
except FileNotFoundError:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your question here...")

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Processing user query
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                if model_type == "Vector":
                    retrieved_docs = vector_search(user_input, top_k=5)
                    answer = "\n".join([f"{i+1}. {doc[1]}" for i, doc in enumerate(retrieved_docs)])
                    context = f""" this is the user query {user_input} this is the context {answer}"""
            # )
                    print(context)
                    answer = service["llm"](context)
                    
                elif model_type == "Semantic":
                    retrieved_docs = vector_search(user_input, top_k=5)  # Retrieve top 5 docs
                    ranked_docs = rerank(user_input, retrieved_docs)
                    answer = "\n".join([
                        f"Rank {i+1}: Score: {score:.4f}\nBody: {doc_info.get('Body', '')}\nAnswer: {doc_info.get('Answer', '')}"
                        for i, ((doc_id, doc_info, doc_text), score) in enumerate(ranked_docs)
                    ])
                    context = f""" this is the user query {user_input} this is the context {answer}"""
            # )
                    print(context)
                    answer = service["llm"](context)
                
                elif model_type == "GraphRAG":
                    retrieved_docs = query_graph_rag(user_input, top_k=5)
                    answer = "\n".join([
                        f"Graph Match {i+1}: Subject: {doc['t.subject']}\nBody: {doc['t.body']}"
                        for i, doc in enumerate(retrieved_docs)
                    ])
                    context = f""" this is the user query {user_input} this is the context {answer}"""
                    print(context)
                    answer = service["llm"](context)


                else:
                    answer = "Invalid model selection."
                    
            except Exception as e:
                answer = f"Failed to process the query. Error: {str(e)}"
            
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

    # Save chat history to a JSON file
    with open(chat_history_file, "w") as file:
        json.dump(st.session_state.messages, file)

# Close DB connection after the session ends (when Streamlit finishes all tasks)
# close_connection()
