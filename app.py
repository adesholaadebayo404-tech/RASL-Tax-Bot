import streamlit as st
import google.generativeai as genai
import os

# 1. API Setup: Fetching key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Google API Key not found. Please configure the GOOGLE_API_KEY secret in your deployment settings.")
    st.stop()

genai.configure(api_key=api_key)

# 2. Search Tool Configuration: Integrating 2026 Google Search retrieval
# dynamic_threshold: 0.3 allows the AI to balance internal knowledge with web searches
tools = [{
    "google_search_retrieval": {
        "dynamic_retrieval_config": {
            "mode": "unspecified",
            "dynamic_threshold": 0.3,
        }
    }
}]

# Load the system persona (ensure system_prompt.md is in your GitHub repo)
try:
    with open("system_prompt.md", "r") as f:
        system_instruction = f.read()
except FileNotFoundError:
    system_instruction = "You are Resilience, the RASL AI assistant providing expert UK tax guidance."

# 3. Model Initialization: Using Gemini 1.5 Flash with the Search tool
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    tools=tools,
    system_instruction=system_instruction
)

# 4. Streamlit UI Setup
st.set_page_config(page_title="Resilience - RASL AI Assistant", page_icon="🛡️")
st.title("🛡️ Resilience")
st.subheader("RASL AI Accounting Assistant")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to RASL. I am Resilience, your AI assistant. I can now search the web for the latest HMRC updates. How may I assist you today?"}
    ]

# Display Conversation History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Chat Interface and Logic
if prompt := st.chat_input("How can I help with your UK tax compliance?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 6. Response Generation with Automatic Function Calling
    with st.chat_message("assistant"):
        try:
            # Enable automatic function calling so the AI can use Search without extra code
            chat = model.start_chat(
                history=[],
                enable_automatic_function_calling=True
            )
            
            # Send message and generate response
            response = chat.send_message(prompt)
            
            # Display and store response
            full_response = response.text
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            # 7. Error Handling: Simple block to prevent app crashes
            error_feedback = f"I apologize, but I encountered an error while processing your request: {str(e)}"
            st.error(error_feedback)
            st.session_state.messages.append({"role": "assistant", "content": error_feedback})

# Professional Footer
st.markdown("---")
st.caption("Resilience is powered by RASL and real-time Google Search. Not legal advice.")
