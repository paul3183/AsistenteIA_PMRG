import os
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

#Para cargar las variables de entorno desde el archivo .env:
load_dotenv()

