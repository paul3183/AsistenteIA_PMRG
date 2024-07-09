import os #interaccion sist. operativo y variables entorno
import requests #biblioteca para realizar solicitudes HTTP a APIs externas
from dotenv import load_dotenv #carga variables de entorno desde un archivo .env en el directorio actual
#Importa Flask y otras herramientas de Flask para crear y manejar la aplicación web
from flask import Flask, request, jsonify, render_template

#carga las variables de entorno
load_dotenv()

#Obtiene la clave de API de OpenAI de las variables de entorno
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
#Definimos la URL base para las solicitudes de chat a la API de OPENAI 
OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions'

#crea una instancia de la aplicación Flask
#static_folder especifica la carpeta donde Flask buscará archivos estáticos
# static_url_path especifica la ruta URL donde se servirán los archivos estáticos
app = Flask(__name__, static_folder='static', static_url_path='/static')

#con este decorador definimos la ruta raíz del proyecto
@app.route('/')
def index():
    #Renderiza y devuelve el archivo index.html ubicado en la carpeta de templates
    return render_template('index.html')

#Define una ruta '/ask' que acepta solicitudes POST para interactuar con la API de OpenAI
@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json['message'].lower() #extrae el mensaje del usuario y lo convertimos en minusculas
    
    #Respuestas personalizadas para preguntas específicas
    personal_questions = ["hola","¿quién eres?", "quién eres?", "quién eres", "¿quien eres?", "quien eres?", "quien eres", "¿qué eres?", "qué eres?", "qué eres", "¿que eres?", "que eres?", "que eres", "¿qué haces?", "¿a qué te dedicas?", "¿qué resuelves?"]
    personal_response = "Hola, soy un modelo de IA entrenado por Paul Martin Ruiz Guardia para asistir en la resolución de dudas y proporcionar información útil."

    #Respuestas personalizadas para preguntas sobre Paul Martin Ruiz Guardia
    paul_questions = ["dime sobre paul ruiz", "quien es paul martin ruiz guardia", "quien es paul ruiz", "quien es paul martin ruiz", "quien es ruiz guardia", "quien te ha entrenado", "¿quién te ha entrenado?", "quién te ha entrenado?", "quien te ha entrenado?", "¿quien te ha entrenado?"]
    paul_response = ("Paul Martin Ruiz Guardia es un Data Engineer con una formación profunda en desarrollo web y manejo de APIs, "
                     "además de ser un experto en Python, Pyspark, y SQL. Especializado en soluciones cloud y tecnologías frontend como ReactJs y Tailwind-Css. "
                     "Paul ha dirigido proyectos innovadores en la gestión de turnos para servicios educativos y ha desarrollado su habilidad en la ciencia de datos y Big Data a través de TECSUP. "
                     "Su experiencia incluye también la gestión de análisis de datos con Polars y Python, así como la educación en plataformas en línea como Udemy. "
                     "Paul es conocido por su capacidad para integrar tecnología avanzada en soluciones prácticas que mejoran los procesos de negocio y educativos.")

    #verifica si la pregunta del usuario coincide con alguna de las preguntas personalizadas de la lista
    if any(question in user_message for question in personal_questions):
        return jsonify({'response': personal_response})
    elif any(question in user_message for question in paul_questions):
        return jsonify({'response': paul_response})

    #prepara los encabezados y los datos para la solicitud HTTP a la API de OpenAI
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }
    data = {
        'model': 'gpt-3.5-turbo', #Especifica el modelo de OpenAI utilizado
        'messages': [{'role': 'user', 'content': user_message}] #Envía el mensaje del usuario
    }
    
    #Realiza una solicitud POST a la API de OpenAI y manejamos las respuestas
    try:
        response = requests.post(OPENAI_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            chat_response = response.json()['choices'][0]['message']['content'].strip()
            return jsonify({'response': chat_response})
        else:
            return jsonify({'error': 'Error al obtener respuesta de OpenAI. Código de estado: ' + str(response.status_code)})
    except Exception as e:
        return jsonify({'error': 'Error en la solicitud: ' + str(e)})

#Punto de entrada para ejecutar la aplicación
if __name__ == '__main__' : 
    app.run(debug = True)
