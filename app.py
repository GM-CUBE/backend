from flask import Flask
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
# secret = os.getenv('JWT_SECRET')

@app.route('/')
def index():
    return '¡Hola, mundo!'

if __name__ == '__main__':
    app.run(debug=True)