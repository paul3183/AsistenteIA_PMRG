import os
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

#Para cargar las variables de entorno desde el archivo .env:
load_dotenv()

#configuración de la clave API y el endpoint de la API de OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions'

app = Flask(__name__)

@app.route('/')
def index():
    #renderiza el template para el formulario del chat:
    return render_template('index.html')

@app.route('ask', methods=['POST'])
def ask():
    user_message = request.json['message']
    headers = {
                'Content-Type': 'application/json', 
                'Authorization': f'Bearer {OPENAI_API_KEY}'
            }
    data = {
            'model' : 'gpt-3.5-turbo', 
            'messages' : [{'role' : 'user', 'content' : user_message}]
            }
    try:
        response = requests.post(OPENAI_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            chat_response = response.json()['choices'][0]['message']['content'].strip()
            return jsonify({'response': chat_response})
        else:
            return jsonify({'error': 'Error al obtener respuesta de OpenAI . Código de estado: ' + str(response.status_code)})
    except Exception as e:
        return jsonify({'error': 'Error en la solicitud: ' + str(e)})    

if __name__ == '__main__' : 
    app.run(debug = True)