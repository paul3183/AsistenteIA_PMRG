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

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json['message'].lower()

    personal_questions = ["hola", "¿quién eres?", "¿qué eres?", "¿qué haces?", "¿a qué te dedicas?", "¿qué resuelves?"]
    personal_response = "Hola, soy un modelo de IA entrenado por Paul Martin Ruiz Guardia para asistir en la resolución de dudas y proporcionar información útil."

    paul_questions = ["quien es paul martin ruiz guardia", "quien es paul ruiz", "quien es paul martin ruiz", "quien es ruiz guardia"]
    paul_response = ("Paul Martin Ruiz Guardia es un Data Engineer con una formación profunda en desarrollo web y manejo de APIs, ...")

    if any(question in user_message for question in personal_questions):
        return jsonify({'response': personal_response})
    elif any(question in user_message for question in paul_questions):
        return jsonify({'response': paul_response})

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
