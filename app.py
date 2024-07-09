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
    user_message = request.json['message'].lower()
    
    # Respuestas personalizadas para preguntas específicas
    personal_questions = ["hola","¿quién eres?", "quién eres?", "quién eres", "¿quien eres?", "quien eres?", "quien eres", "¿qué eres?", "qué eres?", "qué eres", "¿que eres?", "que eres?", "que eres", "¿qué haces?", "¿a qué te dedicas?", "¿qué resuelves?"]
    personal_response = "Hola, soy un modelo de IA entrenado por Paul Martin Ruiz Guardia para asistir en la resolución de dudas y proporcionar información útil."

    # Respuestas personalizadas para preguntas sobre Paul Martin Ruiz Guardia
    paul_questions = ["dime sobre paul ruiz", "quien es paul martin ruiz guardia", "quien es paul ruiz", "quien es paul martin ruiz", "quien es ruiz guardia", "quien te ha entrenado", "¿quién te ha entrenado?", "quién te ha entrenado?", "quien te ha entrenado?", "¿quien te ha entrenado?"]
    paul_response = ("Paul Martin Ruiz Guardia es un Data Engineer con una formación profunda en desarrollo web y manejo de APIs, "
                     "además de ser un experto en Python, Pyspark, y SQL. Especializado en soluciones cloud y tecnologías frontend como ReactJs y Tailwind-Css. "
                     "Paul ha dirigido proyectos innovadores en la gestión de turnos para servicios educativos y ha desarrollado su habilidad en la ciencia de datos y Big Data a través de TECSUP. "
                     "Su experiencia incluye también la gestión de análisis de datos con Polars y Python, así como la educación en plataformas en línea como Udemy. "
                     "Paul es conocido por su capacidad para integrar tecnología avanzada en soluciones prácticas que mejoran los procesos de negocio y educativos.")

    if any(question in user_message for question in personal_questions):
        return jsonify({'response': personal_response})
    elif any(question in user_message for question in paul_questions):
        return jsonify({'response': paul_response})

    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }
    data = {
        'model': 'gpt-3.5-turbo', 
        'messages': [{'role': 'user', 'content': user_message}]
    }
    
    try:
        response = requests.post(OPENAI_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            chat_response = response.json()['choices'][0]['message']['content'].strip()
            return jsonify({'response': chat_response})
        else:
            return jsonify({'error': 'Error al obtener respuesta de OpenAI. Código de estado: ' + str(response.status_code)})
    except Exception as e:
        return jsonify({'error': 'Error en la solicitud: ' + str(e)})

if __name__ == '__main__' : 
    app.run(debug = True)
