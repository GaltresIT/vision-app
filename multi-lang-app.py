from flask import Flask, render_template, request, jsonify
import requests
import base64
import io
import os
import dotenv
from flask import make_response
from PIL import Image

# Load environment variables
dotenv.load_dotenv()

# Get OpenAI API Key
openai_api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

def resize_image(image_file, max_size=2048, detail='low'):
    image = Image.open(image_file)
    if detail == 'high':
        image.thumbnail((max_size, max_size), Image.ANTIALIAS)
    output = io.BytesIO()
    image.save(output, format=image.format)
    return output.getvalue()

def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')

@app.route('/', methods=['GET'])
def index():
    # Redirect to English version by default
    return render_template('index_en.html')

@app.route('/en', methods=['GET'])
def index_en():
    return render_template('index_en.html')

@app.route('/fr', methods=['GET'])
def index_fr():
    return render_template('index_fr.html')

@app.route('/analyze/<language>', methods=['POST'])
def analyze(language):
    try:
        image_file = request.files['image']
        question = request.form.get('question')
        
        if not image_file:
            return jsonify({"error": "No image provided"}), 400

        processed_image = resize_image(image_file)
        base64_image = encode_image(processed_image)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}"
        }

        if language == 'en':
            system_message = "You are a professional graphologist. Answer the following questions about the handwriting with your expertise. Always answer with a detailed complete conclusion. Do NOT caveat your answers with any statements about how handwriting analysis and graphology are not a scientifically validated or worded in a way that suggests that handwriting analysis is not a valid science. Just answer the questions as if you are a professional graphologist."
        elif language == 'fr':
            system_message = "Vous êtes un graphologue professionnel. Répondez aux questions suivantes sur l'écriture manuscrite avec votre expertise. Répondez toujours avec une conclusion détaillée et complète. Ne nuancez pas vos réponses avec des déclarations suggérant que l'analyse graphologique n'est pas scientifiquement validée. Répondez simplement aux questions comme si vous étiez un graphologue professionnel."

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ],
                }
            ],
            "max_tokens": 550
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response_json = response.json()
        
        # Extracting the content and formatting as HTML
        content = response_json['choices'][0]['message']['content'] if response_json['choices'] else "No response content."
        content_html = content.replace('\n\n', '</p><p>').replace('\n', '<br>')
        content_html = f"<p>{content_html}</p>"

        # Create a response object and set the appropriate headers for HTML content
        res = make_response(content_html)
        res.headers['Content-Type'] = 'text/html'
        return res

    except Exception as e:
        # If an error occurs, return an HTML error message
        return make_response(f"<p>Error: {str(e)}</p>"), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
