from flask import Flask, request, jsonify
from flask_cors import CORS

from utils import read_file
from agents import summary_agent, question_agent, study_agent, chat_agent

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # safer CORS

# 🏠 Home route
@app.route('/')
def home():
    return "Cognivra Backend Running 🚀"
@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['file']
    filename = file.filename.lower()

    # 🔥 THIS LINE FIXED
    data, insights = read_file(file)

    # ✅ EXCEL CASE
    if filename.endswith(".xlsx") or filename.endswith(".xls"):
        return jsonify({
            "summary": "Excel analyzed successfully",
            "questions": "",
            "study_notes": "",
            "context": "",
            "table": data,
            "insights": insights
        })

    # ✅ OTHER FILES
    text = data

    summary = summary_agent(text)
    questions = question_agent(text, summary)
    study_notes = study_agent(text, summary)

    return jsonify({
        "summary": summary,
        "questions": questions,
        "study_notes": study_notes,
        "context": text,
        "table": [],
        "insights": {}
    })

    # ✅ Other files
    text = data

    summary = summary_agent(text)
    questions = question_agent(text, summary)
    study_notes = study_agent(text, summary)

    return jsonify({
        "summary": summary,
        "questions": questions,
        "study_notes": study_notes,
        "context": text,
        "table": [],
        "insights": {}
    })
    # ✅ OTHER FILES
    text = read_file(file)

    summary = summary_agent(text)
    questions = question_agent(text, summary)
    study_notes = study_agent(text, summary)

    return jsonify({
        "summary": summary,
        "questions": questions,
        "study_notes": study_notes,
        "context": text,
        "table": [],
        "insights": {}
    })

# 🤖 Chat route
@app.route('/chat', methods=['POST'])
def chat():
    print("🔥 CHAT HIT")  # debug

    data = request.json

    if not data:
        return jsonify({"error": "No data"}), 400

    question = data.get("question")
    context = data.get("context")

    if not question or not context:
        return jsonify({"error": "Missing question/context"}), 400

    try:
        answer = chat_agent(question, context)
    except Exception as e:
        return jsonify({"error": f"Chat error: {str(e)}"}), 500

    return jsonify({"answer": answer})


if __name__ == '__main__':
    app.run(debug=True)