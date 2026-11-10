import streamlit as st
from openai import OpenAI
from datetime import datetime
import json
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="TARS Web UI", page_icon="🤖", layout="centered")
st.title("🤖 TARS Interface")
st.caption("Open-Source AI Assistant")

# Put your key here
API_KEY = st.secrets["OPENROUTER_API_KEY"]

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

# --- PERMANENT MEMORY SETUP ---
MEMORY_FILE = "tars_web_memory.json"

# Load memory from file if it exists
if "messages" not in st.session_state:
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            st.session_state.messages = json.load(f)
    else:
        st.session_state.messages = [
            {"role": "system", "content": "You are TARS from Interstellar. Keep answers witty, concise, and slightly sarcastic. Humor level is 75%."}
        ]

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(st.session_state.messages, f)

# --- DISPLAY CHAT HISTORY ---
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- CHAT INPUT ---
if prompt := st.chat_input("Type your message to TARS..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_memory() # Save immediately after you speak
    
    with st.chat_message("user"):
        st.markdown(prompt)

    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %I:%M %p")
    
    try:
        messages_to_send = st.session_state.messages.copy()
        messages_to_send.append({"role": "system", "content": f"Current time: {current_time}"})

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages_to_send
        )
        
        reply = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(reply)
            
        st.session_state.messages.append({"role": "assistant", "content": reply})
        save_memory() # Save immediately after TARS replies

    except Exception as e:
        st.error(f"Error: {e}")
