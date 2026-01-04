import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

st.title("Chatbot")

with st.sidebar:
    st.title("Hugginface Account")
    hf_email = st.text_input("E-mail")
    hf_password = st.text_input("Password", type="password")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How can i help you"}
    ]

if "chatbot" not in st.session_state and hf_email and hf_password:
    sign = Login(hf_email, hf_password)
    cookies = sign.login()
    st.session_state.chatbot = hugchat.ChatBot(
        cookies=cookies.get_dict()
    )

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

def generate_respone(prompt_input):
    return st.session_state.chatbot.chat(prompt_input).text

if prompt := st.chat_input(disabled=not (hf_email and hf_password)):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            respone = generate_respone(prompt)
            st.write(respone)
    st.session_state.messages.append(
        {"role": "assistant", "content": respone}
    )
