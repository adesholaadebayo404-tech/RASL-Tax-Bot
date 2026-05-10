import streamlit as st
import google.generativeai as genai
import os

# --- 1. Page Configuration ---
st.set_page_config(page_title="Resilience AI", layout="centered")
st.title("Resilience")
st.subheader("Your RASL AI Accounting Assistant")

# --- 2. Initialize AI Model with Search ---
api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    
    # This is the secret sauce for 2026 Search
    tools = [{
        "google_search_retrieval": {
            "dynamic_retrieval_config": {
                "mode": "unspecified",
                "dynamic_threshold": 0.3
            }
        }
    }]
    
    model = genai.GenerativeModel('gemini-1.5-flash', tools=tools)
else:
    st.error("API Key not found. Please check your Secrets.")
    model = None

# --- 3. Chat History Setup ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. Chat Logic ---
if prompt := st.chat_input("How can I help you today?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    if model:
        try:
            # Start chat and enable the search tool automatically
            chat = model.start_chat(history=[], enable_automatic_function_calling=True)
            
            with st.chat_message("assistant"):
                response = chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# --- 5. Footer ---
st.markdown("---")
st.caption("Disclaimer: Resilience provides general guidance and does not constitute formal tax advice.")
