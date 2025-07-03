from flask import Flask, render_template, request, session
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)
app.secret_key = "123456"  # change this to a secure random value

# Configure Gemini model
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


@app.route("/", methods=["GET", "POST"])
def index():
    if "chat_history" not in session:
        session["chat_history"] = []

    typing = False
    chat_history = session["chat_history"]

    if request.method == "POST":
        user_input = request.form["user_input"]
        chat_history.append(("You", user_input))
        session["chat_history"] = chat_history
        typing = True
        session.modified = True

        try:
            prompt = f"You are a helpful C programming tutor. Answer this clearly:\n\n{user_input}"
            response = model.generate_content(prompt).text
        except Exception as e:
            response = f"❌ Error: {e}"

        chat_history.append(("Bot", response))
        session["chat_history"] = chat_history
        typing = False

    return render_template("index.html", chat_history=chat_history, typing=typing)


@app.route("/clear")
def clear():
    session.pop("chat_history", None)
    return "Chat history cleared."


if __name__ == "__main__":
    app.run(debug=True)
