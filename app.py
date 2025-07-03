import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Page config
st.set_page_config(page_title="C Programming Chatbot", page_icon="💬", layout="centered")
st.markdown(
    """
    <style>
        .chat-box {
            background-color: #f1f3f6;
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 10px;
            font-family: 'Segoe UI', sans-serif;
            box-shadow: 1px 1px 6px rgba(0, 0, 0, 0.05);
        }
        .user-msg {
            color: #222;
            font-weight: bold;
        }
        .bot-msg {
            color: #444;
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
        }
        .center-title {
            text-align: center;
            font-size: 26px;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='center-title'>💻 C Programming AI Chatbot</div>", unsafe_allow_html=True)
st.markdown("### Ask me anything about C programming")

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("💬 Your question", placeholder="e.g., Explain malloc vs calloc")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    with st.spinner("Thinking..."):
        try:
            prompt = f"You are a C programming tutor. Answer this clearly:\n\n{user_input}"
            response = model.generate_content(prompt)
            reply = response.text

            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", reply))

            st.toast("✅ Response generated!")

        except Exception as e:
            st.error(f"Gemini API Error: {e}")

# Display chat history
for role, message in st.session_state.chat_history:
    icon = "🧑‍💻" if role == "You" else "🤖"
    role_class = "user-msg" if role == "You" else "bot-msg"
    st.markdown(f"""
        <div class='chat-box'>
            <span class='{role_class}'>{icon} <strong>{role}:</strong></span><br>
            <span class='{role_class}'>{message}</span>
        </div>
    """, unsafe_allow_html=True)
