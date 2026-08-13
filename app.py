from flask import Flask, render_template, request, jsonify
from google import genai
import os

app = Flask(__name__)

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY is not set.")
client = genai.Client(api_key=api_key)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_questions():
    try:
        data = request.get_json()
        source_text = data.get("source", "").strip()
        question_type = data.get("question_type", "Multiple Choice")
        num_questions = int(data.get("num_questions", 3))

        if not source_text:
            return jsonify({"success": False, "message": "Please enter a topic or source material."})

        prompt = f"""You are an expert Question Generator Assistant.
Generate {num_questions} {question_type} questions based on the following topic or text.

Topic/Text:
{source_text}

Requirements:
1. Clearly number every question.
2. Make the questions educational and relevant.
3. Provide correct answers or answer keys where applicable.
4. Keep the formatting clean and easy to read.
5. For Multiple Choice questions, provide four options.
6. For True/False questions, clearly provide the answer.
7. For Fill-in-the-Blank questions, provide the correct answer.
8. For Short Answer questions, provide a concise answer key.
"""
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        return jsonify({"success": True, "result": response.text})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
