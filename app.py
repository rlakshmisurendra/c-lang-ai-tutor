from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
model = genai.GenerativeModel("gemini-1.5-flash")


@app.route("/", methods=["GET", "POST"])
def index():
    chat_history = []
    typing = False

    if request.method == "POST":
        user_input = request.form["user_input"]
        chat_history.append(("You", user_input))
        typing = True

        try:
            prompt = f"You are a C programming tutor. Answer clearly:\n{user_input}"
            response = model.generate_content(prompt).text
        except Exception as e:
            response = f"⚠️ Error: {e}"

        chat_history.append(("Bot", response))
        typing = False

    return render_template("index.html", chat_history=chat_history, typing=typing)


if __name__ == "__main__":
    app.run(debug=True)
