import streamlit as st
from groq import Groq

# Page config
st.set_page_config(
    page_title="DataMind",
    page_icon="🤖",
    layout="centered"
)

# App title
st.title("🤖 DataMind")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# If no API key entered yet show input
if st.session_state.api_key == "":
    st.subheader("🔑 Enter Your Groq API Key")
    st.markdown("Get your free API key at [console.groq.com](https://console.groq.com)")
    
    api_key_input = st.text_input(
        "Groq API Key:", 
        type="password",
        placeholder="paste your groq api key here..."
    )
    
    if st.button("Start Chatting! 🚀", use_container_width=True):
        if api_key_input:
            st.session_state.api_key = api_key_input
            st.rerun()
        else:
            st.error("Please enter your API key first!")
else:
    # Show logout button in sidebar
    with st.sidebar:
    	st.markdown("### ⚙️ Settings")
    	st.markdown("**Model:** Llama 3.3 70B")
    	st.markdown("**Provider:** Groq")
    	st.divider()
    
    	# New Chat button
    	if st.button("➕ New Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    	st.divider()
    
    	if st.button("🔑 Change API Key", use_container_width=True):
            st.session_state.api_key = ""
            st.session_state.messages = []
            st.rerun()
    	if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )
        with st.chat_message("user"):
            st.markdown(prompt)

        # Groq API call
        client = Groq(api_key=st.session_state.api_key)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    max_tokens=1000
                )
                answer = response.choices[0].message.content
                st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )