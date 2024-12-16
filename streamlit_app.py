import streamlit as st
import openai 

st.title("ChatGPT Clone")

openai.api_key = "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"

if "openai_model" not in st.session_state:
  st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
  st.session_state.messages = []

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
  with st.chat_message("user"):
    st.markdown(prompt)
  st.session_state.messages.append({"role": "user", "content": prompt})

  with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    for response in openai.completions.create(
      model=st.session_state["openai_model"],
      messages = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
      ],
      stream=True
    ):
      full_response += response.choices[0].delta.get("content", "")
      message_placeholder.markdown(full_response + "|")
    message_placeholder.markdown(full_response)
  st.session_state.messages.append({"role": "assistant", "content": full_response})