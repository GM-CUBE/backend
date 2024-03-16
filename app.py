from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS
from dotenv import load_dotenv
import os

from my_lib.general import crud_template, is_none
# import my_lib.database
from my_lib.database import crate_table_row, read_all_table, update_table_row, delete_table_row

# -----------------------------------------------------------------------------

load_dotenv()

app = Flask(__name__)
CORS(app)
JWTManager(app)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

URI = os.getenv('URI')

# -----------------------------------------------------------------------------

@app.route('/')
def index():
    return '¡Hola, mundo!'


@app.route('/prueba_all', methods=['POST', 'GET'])
@app.route('/prueba_all/<int:_id>', methods=['GET', 'PUT', 'DELETE'])
@crud_template(request, ['campo1', 'campo2', 'campo3', 'campo4'], ['campo1'])
def prueba_post(_id=None):

    if request.method == 'POST':
        campo1 = request.json['campo1']
        campo2 = request.json['campo2']
        campo3 = request.json['campo3']
        campo4 = request.json['campo4']

    if is_none(_id):
        return jsonify({
            "message": "Datos recibidos correctamente",
            "id": "nada",
            "hola": request.method
        }), 200
    
    else:
        return jsonify({
            "message": "Datos recibidos correctamente",
            "id": _id,
            "hola": request.method
        }), 200

if __name__ == '__main__':
    app.run(debug=True)