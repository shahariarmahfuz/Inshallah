import os
from flask import Flask, request, jsonify
from google.generativeai import GenerativeModel

genai.configure(api_key=os.getenv("API_KEY"))

app = Flask(__name__)

# Gemini Pro মডেল কনফিগারেশন:
config = {
    'temperature': 0.7,
    'top_k': 40,
    'top_p': 0.95,
    'max_output_tokens': 800
}

# নিরাপত্তা সেটিংস:
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]

# মডেল তৈরি:
model = GenerativeModel(model="models/chat-bison-001",
                       generation_config=config,
                       safety_settings=safety_settings)

# API Endpoint:
@app.route('/api/gen', methods=['GET'])
def generate_response():
    prompt = request.args.get('prompt')
    if not prompt:
        return jsonify({"error": "No prompt provided"})

    response = model.generate_text(prompt=prompt)

    if response.is_error:
        return jsonify({"error": f"Error generating response: {response.error}"})

    return jsonify({"response": response.candidates[0].output})

# অ্যাপ্লিকেশন চালু:
if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
    
