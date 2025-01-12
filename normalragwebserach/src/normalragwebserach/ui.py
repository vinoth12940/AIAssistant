import streamlit as st
from normalragwebserach.crew import Normalragwebserach
import json

def extract_response(result):
    """Extract the actual response from the crew result"""
    try:
        if isinstance(result, str):
            try:
                result = json.loads(result)
            except json.JSONDecodeError:
                return result.strip()

        if isinstance(result, dict) and 'tasks_output' in result:
            conversation_output = result['tasks_output'][0]
            if isinstance(conversation_output, dict):
                return conversation_output.get('raw', '')
            elif hasattr(conversation_output, 'raw'):
                return conversation_output.raw
        return str(result).strip()
    except Exception:
        return str(result).strip()

def run_ui():
    # Page configuration
    st.set_page_config(
        page_title="AI Research Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Modern, Dark Theme CSS
    st.markdown("""
        <style>
        /* Base theme */
        :root {
            --primary-bg: #1E1E1E;
            --secondary-bg: #2D2D2D;
            --chat-bg: #383838;
            --user-msg-bg: #2B5C34;
            --bot-msg-bg: #1E3A8A;
            --text-color: #FFFFFF;
            --input-bg: #2D2D2D;
            --accent: #4CAF50;
        }

        /* Main app container */
        .stApp {
            background-color: var(--primary-bg);
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: var(--secondary-bg);
            padding: 2rem 1rem;
        }

        .sidebar-content {
            background: rgba(255, 255, 255, 0.05);
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        }

        /* Chat container */
        .main-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            background: var(--chat-bg);
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        /* Message containers */
        [data-testid="stChatMessage"] {
            background: transparent !important;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 15px;
            color: var(--text-color);
        }

        /* User message */
        [data-testid="stChatMessage"][data-testid="user"] {
            background: var(--user-msg-bg) !important;
            margin-left: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Assistant message */
        [data-testid="stChatMessage"][data-testid="assistant"] {
            background: var(--bot-msg-bg) !important;
            margin-right: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Input container */
        .stChatInputContainer {
            background-color: var(--input-bg);
            padding: 1rem;
            border-radius: 10px;
            margin-top: 2rem;
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: 90%;
            max-width: 1000px;
            z-index: 1000;
        }

        /* Input field */
        .stChatInput input {
            background-color: var(--secondary-bg);
            color: var(--text-color);
            border: 1px solid var(--accent);
            border-radius: 8px;
            padding: 0.8rem;
        }

        .stChatInput input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
        }

        /* Buttons */
        .stButton button {
            background-color: var(--accent);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .stButton button:hover {
            opacity: 0.9;
            transform: translateY(-2px);
        }

        /* Welcome message */
        .welcome-container {
            text-align: center;
            padding: 3rem;
            color: var(--text-color);
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            margin: 2rem 0;
        }

        .welcome-container h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            background: linear-gradient(45deg, #4CAF50, #2196F3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--primary-bg);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--accent);
            border-radius: 4px;
        }

        /* Message content */
        .stMarkdown {
            color: var(--text-color) !important;
        }

        /* Avatar styling */
        .stChatMessage .avatar {
            width: 40px !important;
            height: 40px !important;
            border-radius: 50%;
            border: 2px solid var(--accent);
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("""
            <div style='text-align: center; margin-bottom: 2rem;'>
                <h1 style='color: #4CAF50; font-size: 1.8rem;'>🤖 AI Assistant</h1>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
        st.markdown("### Features")
        st.markdown("""
            • 💬 Natural Conversations
            • 🔍 Smart Search
            • 🧠 Context Awareness
            • ⚡ Quick Responses
        """)
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

    # Initialize session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'crew' not in st.session_state:
        st.session_state.crew = Normalragwebserach()

    # Main chat container
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

    # Welcome message
    if not st.session_state.chat_history:
        st.markdown("""
            <div class='welcome-container'>
                <h1>Welcome to AI Assistant</h1>
                <p style='font-size: 1.2rem; color: #CCCCCC;'>
                    How can I help you today?
                </p>
            </div>
        """, unsafe_allow_html=True)

    # Chat messages
    for message in st.session_state.chat_history:
        role, content = message
        with st.chat_message(role, avatar="👤" if role == "user" else "🤖"):
            st.markdown(f"<div style='color: white;'>{content}</div>", unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        with st.chat_message("user", avatar="👤"):
            st.markdown(f"<div style='color: white;'>{prompt}</div>", unsafe_allow_html=True)
        st.session_state.chat_history.append(("user", prompt))

        try:
            with st.spinner("Processing..."):
                result = st.session_state.crew.crew().kickoff(inputs={'topic': prompt})
                response = extract_response(result)
            
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(f"<div style='color: white;'>{response}</div>", unsafe_allow_html=True)
            st.session_state.chat_history.append(("assistant", response))

        except Exception as e:
            st.error("Something went wrong. Please try again.")

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    run_ui() 