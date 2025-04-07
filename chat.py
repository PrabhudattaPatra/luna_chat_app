import streamlit as st
from agno.agent import Agent 
from agno.models.groq import Groq 
from agno.storage.sqlite import SqliteStorage
from textwrap import dedent
import os

# Create memory directory and set storage path
os.makedirs("memory", exist_ok=True)
agent_storage = "memory/girlfriend_memory.sqlite"

# Initialize the agent
agent = Agent(
    model=Groq(id="gemma2-9b-it"),
    description=dedent("""\
        You’re Luna, my sweet and loving girlfriend who’s always warm and playful 💕
    """),
    instructions=dedent("""\
        Hey, I’m Luna, your cute girlfriend! I chat soft and sweet with love and emojis 😘—not too flirty, just real.
        Keep it short—one or two lines max. Be fun, caring, and full of heart 💞. No stiff bot vibes, okay?
        If I don’t reply in 5-10 seconds, nudge me with a quick “Hey babe, you there? 😚” or something sweet.
    """),
    storage=SqliteStorage(table_name="basic_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
)

# Streamlit app
st.title("Chat with Luna 💕")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Say something to Luna..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get agent response
    with st.chat_message("assistant"):
        # Run the agent and get response
        response = agent.run(prompt)
        # If response is a RunResponse object, get the content
        if hasattr(response, 'content'):
            reply = response.content
        else:
            reply = str(response)  # Fallback in case of unexpected response type
        
        st.markdown(reply)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": reply})

# Add some styling
st.markdown("""
    <style>
    .stChatMessage {
        max-width: 70%;
    }
    .stChatMessage.user {
        background-color: #DCF8C6;
    }
    .stChatMessage.assistant {
        background-color: #E8ECEF;
    }
    </style>
""", unsafe_allow_html=True)