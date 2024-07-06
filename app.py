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
