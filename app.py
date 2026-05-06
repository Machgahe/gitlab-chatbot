import streamlit as st
from chatbot import ask

st.set_page_config(page_title="GitLab Handbook Chatbot", page_icon="🦊")

st.title("🦊 GitLab Handbook Chatbot")
st.caption("Ask me anything about GitLab's values, culture, engineering, and more.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("📚 Sources"):
                for source in message["sources"]:
                    st.write(source)

# Chat input
if prompt := st.chat_input("Ask about GitLab..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get and show bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = ask(prompt)
        st.markdown(result["answer"])
        with st.expander("📚 Sources"):
            for source in result["sources"]:
                st.write(source)

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sources": result["sources"]
    })