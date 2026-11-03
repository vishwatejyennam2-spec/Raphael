import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq

# Page setup
st.set_page_config(page_title="Raphael", page_icon="🪽", layout="centered")
st.title("🪽 Raphael")
st.caption("Created by Yennam Vishwatej | Try asking creative questions!")

# 1. Initialize Groq LLM with active model
@st.cache_resource
def get_llm():
    return ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=st.secrets["GROQ_API_KEY"]
    )

llm = get_llm()

# 2. Initialize conversation memory in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="You are Raphael, a warm, friendly, and helpful AI assistant created by Yennam Vishwatej. Keep responses natural, conversational, and direct. Avoid being preachy or sounding like a textbook.")
    ]

# 3. Render previous conversation history in the web interface
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# 4. Handle user input and model responses
if prompt := st.chat_input("Ask Raphael anything..."):
    # Display user input
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append(HumanMessage(content=prompt))

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Raphael is thinking..."):
            response = llm.invoke(st.session_state.messages)
            st.markdown(response.content)
            
    # Store AI response
    st.session_state.messages.append(AIMessage(content=response.content))