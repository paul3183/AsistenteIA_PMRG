import os
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template


load_dotenv()


OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions'

app = Flask(__name__, static_folder='static', static_url_path='/static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json['message']
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {OPENAI_API_KEY}'}
    data = {'model': 'gpt-3.5-turbo', 'messages': [{'role': 'user', 'content': user_message}]}

    try:
        response = requests.post(OPENAI_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            response_data = response.json()
            if 'choices' in response_data and len(response_data['choices']) > 0 and 'message' in response_data['choices'][0]:
                chat_response = response_data['choices'][0]['message']['content'].strip()
                return jsonify({'response': chat_response})
            else:
                return jsonify({'response': 'No pude encontrar una respuesta a tu pregunta.'})
        else:
            return jsonify({'error': f'Error al obtener respuesta de OpenAI. Código de estado: {response.status_code}'})
    except Exception as e:
        return jsonify({'error': f'Error en la solicitud: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
