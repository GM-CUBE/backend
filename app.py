from flask import Flask, request, jsonify, abort
from dotenv import load_dotenv
import os





app = Flask(__name__)
load_dotenv()
# secret = os.getenv('JWT_SECRET')

BASE_URL='/api/'
valid = ['name', 'last_Name', 'email', 'password']

# ADD USER





@app.route('/')
def index():
    return '¡Hola, mundo!'


if __name__ == '__main__':
    app.run(debug=True)