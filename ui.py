import streamlit as st
import requests

st.title("Homelab Zim Assistant")

if "history" not in st.session_state:
    st.session_state.history = []

question = st.chat_input("Ask something...")

for q, a in st.session_state.history:
    st.chat_message("user").write(q)
    st.chat_message("assistant").write(a)

if question:
    st.chat_message("user").write(question)
    with st.spinner("Searching zims..."):
        r = requests.post("http://localhost:8000/ask", json={"question": question})
        answer = r.json()["answer"]
    st.chat_message("assistant").write(answer)
    st.session_state.history.append((question, answer))
