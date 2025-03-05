# import streamlit as st
# import requests

# # Center the radio buttons without the "Select Model" text
# st.markdown("<h3 style='text-align: center;'> </h3>", unsafe_allow_html=True)

# # Center the radio buttons directly
# model_choice = st.radio("", ["Vector Search", "Semantic Ranker", "GraphRAG"], index=0, horizontal=True)

# st.title("Ticket Resolution Assistant")
# st.write("Ask me about any issue, and I'll find the best solution!")

# # User input
# user_query = st.text_input("Enter your question:")

# if st.button("Get Solution"):
#     if user_query:
#         # Map model choice to API parameters
#         model_map = {
#             "Vector Search": "vector",
#             "Semantic Ranker": "semantic",
#             "GraphRAG": "graphrag"
#         }
#         selected_model = model_map[model_choice]

#         # Call FastAPI endpoint
#         with st.spinner("Fetching solution..."):
#             response = requests.post("http://localhost:8000/query/", json={
#                 "ticket_query": user_query,
#                 "model": selected_model
#             })

#             if response.status_code == 200:
#                 result = response.json().get("response", "No response received.")
#                 st.success("✅ Solution Found:")
#                 st.write(result)
#             else:
#                 st.error("❌ Failed to fetch the solution. Please try again.")
#     else:
#         st.warning("⚠️ Please enter a valid query.")

# # Sidebar for metadata or logs
# st.sidebar.header("🔍 Query Details")
# st.sidebar.write(f"User Query: {user_query}")
# st.sidebar.write(f"Selected Model: {model_choice}")

import streamlit as st
import requests
import json

# Streamlit UI setup
st.set_page_config(page_title="Ticket Resolution Assistant", layout="wide")
st.title("🎫 Ticket Resolution Assistant")
st.markdown("Chat with the AI Assistant for ICM Ticket Resolution.")

# Sidebar for model selection
with st.sidebar:
    st.header("⚙️ Configuration")
    model_type = st.selectbox("Select Model Type:", ["Vector", "Semantic", "GraphRAG"])
    # api_url = st.text_input("API Endpoint:", "http://localhost:8000/query")

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

    # API request
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(api_url, json={"model": model_type, "query": user_input})
                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer found.")
                else:
                    answer = f"Error: {response.status_code} - {response.text}"
            except Exception as e:
                answer = f"Failed to connect to the API. Error: {str(e)}"

            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

    # Save chat history to a JSON file
    with open(chat_history_file, "w") as file:
        json.dump(st.session_state.messages, file)
