from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv
import google.generativeai as genai
import markdown2
from markupsafe import Markup

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)
chat_history = []

@app.route("/", methods=["GET", "POST"])
def index():
    global chat_history
    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()
        if user_input:
            prompt = f"You are a C programming tutor. Answer this clearly with example code if needed:\n\n{user_input}"
            try:
                response = model.generate_content(prompt)
                reply_raw = response.text.strip()
                reply_html = markdown2.markdown(reply_raw, extras=["fenced-code-blocks"])
            except Exception as e:
                reply_html = f"<div class='text-danger'>❌ Gemini API Error: {e}</div>"

            chat_history.append(("You", Markup.escape(user_input)))
            chat_history.append(("Bot", Markup(reply_html)))

        return redirect(url_for("index"))
    return render_template("index.html", chat_history=chat_history)

if __name__ == "__main__":
    app.run(debug=True)
