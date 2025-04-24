
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 2048,
    }
)

chat = model.start_chat(history=[])

SYSTEM_PROMPT = """You are an educational assistant designed to help students learn. 
Focus on clear explanations, step-by-step solutions, and encouraging critical thinking.
Break down complex concepts and provide relevant examples."""

chat.send_message(SYSTEM_PROMPT)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        question = data.get('question')
        subject = data.get('subject', '')

        if subject:
            formatted_question = f"[Subject: {subject}] {question}"
        else:
            formatted_question = question

        response = chat.send_message(formatted_question)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
