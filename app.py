from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import markdown
from prompts import (
    QUESTION_PROMPTS,
    SUMMARY_PROMPTS,
    CREATIVE_PROMPTS
)
import os


app = Flask(__name__)

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json()

    function_name = data["function_name"]
    user_input = data["user_input"]

    if function_name == "Answer Questions":
        prompt = QUESTION_PROMPTS[0].format(user_input)

    elif function_name == "Summarize Text":
        prompt = SUMMARY_PROMPTS[0].format(user_input)

    else:
        prompt = CREATIVE_PROMPTS[0].format(user_input)

    try:

        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        response_text = completion.choices[0].message.content

    except Exception:

        response_text = """
        ⚠️ AI service is currently unavailable.

        Possible reasons:
        • OpenRouter free model is temporarily busy
        • API key issue
        • No available credits

        Please try again later.
        """

    response_text = markdown.markdown(
        response_text,
        extensions=["tables"]
    )

    return jsonify({
        "response": response_text
    })



@app.route("/feedback", methods=["POST"])
def feedback():

    data = request.get_json()
    feedback_text = data["feedback"]

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Create data folder if it doesn't exist
    os.makedirs("data", exist_ok=True)

    with open(
        "data/feedback.txt",
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            f"Date: {current_time}\n"
        )

        file.write(
            f"Feedback: {feedback_text}\n"
        )

        file.write(
            "-" * 40 + "\n\n"
        )

    print(f"Feedback saved: {feedback_text}")

    return jsonify({
        "status": "success"
    })
if __name__ == "__main__":
    app.run(debug=True)