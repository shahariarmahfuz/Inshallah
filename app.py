import os
from flask import Flask, request, jsonify
from google.generativeai import GenerativeModel

genai.configure(api_key=os.getenv("API_KEY"))

app = Flask(__name__)

# Gemini Pro মডেল কনফিগারেশন:
config = {
    'temperature': 0.7,      # উত্তরের ক্রিয়েটিভিটি নিয়ন্ত্রণ করে (0 - 1)
    'top_k': 40,             # উত্তর জেনারেট করার সময় বিবেচনা করার শব্দের সংখ্যা
    'top_p': 0.95,            # উত্তর জেনারেট করার সময় সম্ভাব্যতা বণ্টন নিয়ন্ত্রণ করে
    'max_output_tokens': 800  # উত্তরের সর্বোচ্চ দৈর্ঘ্য
}

# নিরাপত্তা সেটিংস: (ক্ষতিকর কন্টেন্ট প্রতিরোধ)
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
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
