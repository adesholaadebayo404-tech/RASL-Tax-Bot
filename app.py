import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Resilience - RASL AI Assistant",
    page_icon="https://img1.wsimg.com/isteam/ip/132a448b-d29c-444c-9e47-ce47021f0d8d/RAS%20Logo.png",
    layout="centered"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stChatFloatingInputContainer {
        background-color: #ffffff;
    }
    .st-emotion-cache-1c7n2ka {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1 {
        color: #1a365d;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #1a365d;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Path to the system prompt
SYSTEM_PROMPT_PATH = "system_prompt.md"

def load_system_prompt():
    try:
        with open(SYSTEM_PROMPT_PATH, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "You are Resilience, the AI Assistant for RASL (Resilience Accounting Service Limited). Provide expert guidance on UK tax compliance, VAT, and Corporation Tax in a professional, authoritative, supportive, and resilient tone."

# Initialize AI model
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    
    # This line creates the search tool
    tools = [{"google_search": {}}]
    
    # This line tells the model to use that tool
    model = genai.GenerativeModel('gemini-1.5-flash', tools=tools)
else:
    model = None

# App Title and Header
st.image("https://img1.wsimg.com/isteam/ip/132a448b-d29c-444c-9e47-ce47021f0d8d/RAS%20Logo.png", width=100)
st.title("Resilience")
st.subheader("Your RASL AI Accounting Assistant")

# Sidebar
with st.sidebar:
    st.image("https://img1.wsimg.com/isteam/ip/132a448b-d29c-444c-9e47-ce47021f0d8d/RAS%20Logo.png")
    st.title("RASL")
    st.markdown("""
    **Resilience Accounting Service Limited**
    
    Building stable foundations for UK businesses.
    
    ---
    ### Services
    - VAT Compliance
    - Corporation Tax
    - Business Planning
    - Professional Consultations
    """)
    
    if st.button("Book a Consultation"):
        st.info("Redirecting to booking system...")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Initial greeting
    initial_greeting = "Welcome to RASL. I am Resilience, your AI assistant. I am here to help ensure your business remains compliant and resilient by providing guidance on UK tax, VAT, and Corporation Tax. How may I assist you today?"
    st.session_state.messages.append({"role": "assistant", "content": initial_greeting})

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("How can I help with your UK tax compliance?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if model:
            try:
                system_prompt = load_system_prompt()
                chat = model.start_chat(history=[])
                full_prompt = f"System Instruction: {system_prompt}\n\nUser: {prompt}"
                response = chat.send_message(full_prompt)
                assistant_response = response.text
            except Exception as e:
                assistant_response = f"I apologize, but I am experiencing a technical difficulty. (Error: {str(e)})"
        else:
            # Fallback mock responses
            if "vat" in prompt.lower():
                assistant_response = "In the UK, you generally must register for VAT if your taxable turnover exceeds £90,000. For specific advice, I recommend a professional consultation."
            else:
                assistant_response = "I understand your query. As Resilience, I recommend a consultation for definitive advice tailored to your business."

        st.markdown(assistant_response)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

st.markdown("---")
st.caption("Disclaimer: This AI assistant provides general guidance only and does not constitute professional tax or legal advice.")
