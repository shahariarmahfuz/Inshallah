import os
from flask import Flask, request, jsonify
import google.generativeai as genai

# 1. API Key কনফিগারেশন:
genai.configure(api_key=os.getenv("API_KEY"))  # API Key পরিবেশ ভেরিয়েবল থেকে পড়া

# 2. Flask অ্যাপ তৈরি:
app = Flask(__name__)

# 3. Gemini Pro মডেল কনফিগারেশন:
# (এই সেটিংসগুলি আপনার প্রয়োজন অনুসারে পরিবর্তন করতে পারেন)
config = {
    'temperature': 0.7,  # উত্তরের ক্রিয়েটিভিটি নিয়ন্ত্রণ করে (0 - 1)
    'top_k': 40,        # উত্তর জেনারেট করার সময় বিবেচনা করার শব্দের সংখ্যা
    'top_p': 0.95,       # উত্তর জেনারেট করার সময় সম্ভাব্যতা বণ্টন নিয়ন্ত্রণ করে
    'max_output_tokens': 800  # উত্তরের সর্বোচ্চ দৈর্ঘ্য
}

# 4. নিরাপত্তা সেটিংস: (ক্ষতিকর কন্টেন্ট প্রতিরোধ)
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]

# 5. মডেল তৈরি:
model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=config,
    safety_settings=safety_settings
)

# 6. API Endpoint:
@app.route('/api/gen', methods=['GET'])
def generate_response():
    prompt = request.args.get('prompt')  # URL থেকে প্রম্পট পড়া
    if not prompt:
        return jsonify({"error": "No prompt provided"})  # প্রম্পট না থাকলে ত্রুটি বার্তা

    response = model.generate_text(prompt=prompt)  # মডেল থেকে উত্তর জেনারেট করা

    # 7. ত্রুটি ব্যবস্থাপনা:
    if response.is_error:
        return jsonify({"error": f"Error generating response: {response.error}"})

    # 8. JSON Response:
    return jsonify({"response": response.result})  # উত্তর JSON ফরম্যাটে পাঠানো

# 9. অ্যাপ্লিকেশন চালু:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Render-এর জন্য পোর্ট সেটিং
    app.run(host='0.0.0.0', port=port)  # সব নেটওয়ার্ক ইন্টারফেসে শোনা
