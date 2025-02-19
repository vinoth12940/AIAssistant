import streamlit as st
from normalragwebserach.crew import Normalragwebserach
import json

def extract_response(result):
    """Extract the actual response from the crew result"""
    try:
        # Convert result to string and clean it up
        response = str(result).strip()
        
        # If it's a knowledge base result, format it nicely
        if '```' in response and any(field in response for field in ['Index,Customer Id,First Name']):
            # Extract CSV data
            csv_data = response.split('```')[1].strip()
            headers = csv_data.split('\n')[0].split(',')
            values = csv_data.split('\n')[1].split(',')
            
            # Create formatted response
            formatted_response = "**Customer Information:**\n\n"
            for header, value in zip(headers, values):
                formatted_response += f"**{header.strip()}:** {value.strip()}\n"
            return formatted_response
            
        # For analysis results, only return if explicitly requested
        if 'TYPE:' in response and 'REASON:' in response:
            return response
            
        # For SKIP messages, ignore them
        if response.startswith('SKIP:'):
            return ''
            
        # Remove any remaining markdown code blocks
        if '```' in response:
            response = response.split('```')[-2] if len(response.split('```')) > 2 else response.replace('```', '')
            
        return response.strip()
        
    except Exception as e:
        return f"I apologize, but I encountered an error processing the response. Error: {str(e)}"

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
            --chat-bg: #1E1E1E;
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
            color: var(--text-color);
        }

        /* User message container - move entire container to right */
        [data-testid="stChatMessage"][data-testid="user"] {
            display: flex !important;
            flex-direction: row-reverse !important;
            width: 100% !important;
        }

        [data-testid="stChatMessage"][data-testid="user"] > div:first-child {
            margin-left: auto !important;
            margin-right: 0 !important;
        }

        /* Keep rest of the styling same */
        [data-testid="stChatMessage"][data-testid="user"] > div {
            background: var(--secondary-bg) !important;
            border-radius: 15px !important;
            padding: 0.8rem 1rem;
            max-width: 80%;
        }

        /* Assistant message - align to left */
        [data-testid="stChatMessage"][data-testid="assistant"] {
            display: flex !important;
            align-items: flex-start !important;
            gap: 0.5rem !important;
        }
        
        [data-testid="stChatMessage"][data-testid="assistant"] .stMarkdown {
            background: var(--chat-bg) !important;
            border-radius: 20px !important;
            padding: 0.8rem 1rem;
            display: inline-block;
            max-width: 80%;
            text-align: left;
        }

        /* Hide avatars */
        [data-testid="stChatMessage"] .avatar {
            display: none !important;
        }

        /* Input container */
        .stChatInputContainer {
            background-color: var(--chat-bg);
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

        /* Add this new CSS rule for the bottom block container */
        [data-testid="stBottomBlockContainer"] {
            background-color: var(--chat-bg) !important;
        }

        /* Add this CSS at the top with your other styles */
        [data-testid="stChatMessage"][data-testid="user"] {
            margin-left: auto !important;
            width: fit-content !important;
        }

        [data-testid="stChatMessage"][data-testid="user"] {
            flex-direction: row-reverse !important;
            margin-left: auto;
        }
        [data-testid="stChatMessage"][data-testid="user"] .stMarkdown {
            width: 100%;
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
    #st.markdown("<div class='main-container'>", unsafe_allow_html=True)

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

    # Chat messages from history
    for message in st.session_state.chat_history:
        role, content = message
        if role == "user":
            with st.chat_message(role):
                st.markdown(content)  # Just display the content, let Streamlit handle the layout
        else:
            with st.chat_message(role):
                st.markdown(f"""<div style="background-color: #383838; padding: 10px 15px; border-radius: 15px;">
                    {content}
                </div>""", unsafe_allow_html=True)

    # Chat input and new messages
    if prompt := st.chat_input("Type your message here..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(f"""<div style="display: flex; justify-content: flex-end; width: 100%;">
                <div style="background-color: #2D2D2D; padding: 10px 15px; border-radius: 15px; max-width: 80%;">
                    {prompt}
                </div>
            </div>""", unsafe_allow_html=True)
        st.session_state.chat_history.append(("user", prompt))

        try:
            with st.spinner("Processing..."):
                result = st.session_state.crew.kickoff(prompt)
                response = extract_response(result)
                if not response or response.isspace():
                    response = "I apologize, but I couldn't generate a proper response. Please try asking your question in a different way."
            
            # Display assistant message
            with st.chat_message("assistant"):
                st.markdown(f"""<div style="display: flex; justify-content: flex-start; width: 100%;">
                    <div style="background-color: #383838; padding: 10px 15px; border-radius: 15px; max-width: 80%;">
                        {response}
                    </div>
                </div>""", unsafe_allow_html=True)
            st.session_state.chat_history.append(("assistant", response))

        except Exception as e:
            error_msg = f"I apologize, but something went wrong: {str(e)}\nPlease try again or rephrase your question."
            st.error(error_msg)
            st.session_state.chat_history.append(("assistant", error_msg))

    st.markdown("</div>", unsafe_allow_html=True)

    # Add this CSS for user messages, keep all other CSS unchanged
    st.markdown("""
        <style>
            [data-testid="stChatMessage"][data-testid="user"] {
                flex-direction: row-reverse !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Add this CSS at the end of run_ui() function
    st.markdown("""
        <style>
        .stChatMessage:has([data-testid="stChatMessageAvatarUser"]) {
            display: flex;
            flex-direction: row-reverse;
            align-items: end;
        }

        [data-testid="stChatMessageAvatarUser"] + [data-testid="stChatMessageContent"] {
            text-align: right;
        }
        </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    run_ui() 