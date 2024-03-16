from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS
from dotenv import load_dotenv
import os, re

from my_lib.general import crud_template, is_none
from my_lib.database import DB_interface

# -----------------------------------------------------------------------------

load_dotenv()

app = Flask(__name__)
CORS(app)
JWTManager(app)
database = DB_interface()

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

URI = os.getenv('URI')

# -----------------------------------------------------------------------------

@app.route('/signup', methods=['POST'])
@crud_template(request, ['FirstName', 'LastName', 'Age', 'Username', 'Password', 'Email'])
def signup():

    FirstName = request.json['FirstName'] 
    LastName = request.json['LastName'] 
    Age = request.json['Age'] 
    Username = request.json['Username'] 
    Password = request.json['Password'] 
    Email = request.json['Email']  

    ClaseDB.AddUser(FirstName, LastName, Age, Username, Password, Email)

    #todo ENVIAR EL CORREO DE VERIFICACION

    return jsonify({
        "message": "Agregado correctamente"
    }), 200


@app.route('/login', methods=['GET', 'POST'])
@crud_template(request, ['username', 'password'])
def login():

    username = request.json['Username']
    password = request.json['Password']

    user = ClaseDB.SearchUser(username, password)
    #todo JWT

    if user != None:

        return jsonify({
            "message": "Encontrado",
            "user": user
        }), 200
    
    else:

        return jsonify({
            "message": "Datos incorrectos",
            "user": None
        }), 401


@app.route('/gameover/<int:_id>', methods=['GET', 'POST'])
@crud_template(request, ['Prestige', 'Coins', 'Victory'])
def juegoterminado(_id):

    newPrestige = request.json['Prestige']
    newCoins = request.json['Coins']
    isVictory = request.json['Victory']

    ClaseDB.JuegoTerminado(_id, newPrestige, newCoins, isVictory)

    user = ClaseDB.GetUser(_id)

    return jsonify({
        "message": "Listo",
        "user": user
    }), 200


@app.route('/shortcut/<int:_idgame>', methods=['POST'])
@crud_template(request, ['Shortcut'])
def shortcut(_idgame):

    shortcut = request.json['Shortcut']
    _idshort = ClaseDB.BusarShortCut(shortcut)
    
    ClaseDB.ChangeCoins(_idgame, _idshort)
    
    ClaseDB.Shortcut_Game(_idshort, _idgame)


@app.route('/history/<int:_id>', methods=['GET'])
def history(_id):
    history = ClaseDB.History(_id)

    return jsonify({
        "history": history
    }), 200


@app.route('/answer/<int: _idGame>/<int: _idQuestion>', methods=['POST'])
@crud_template(request, ['Time', 'Answer'])
def answer(_idGame, _idQuestion):

    time = request.json['Time']
    answer = request.json['Answer']

    #todo validacion de respuesta

    regex = ClaseDB.GetAnswer(_idQuestion)

    result = re.search(regex, answer)

    if result:
        isCorrect = True
    else:
        isCorrect = False

    ClaseDB.AddAnswer(_idQuestion, _idGame, time, answer, isCorrect)


@app.route('/queue/<int:_id>', methods=['GET'])
def queue(_id):
    
    user = ClaseDB.SearchUser(_id)
    found = ClaseDB.SearchQueue(user['Prestigio'])

    if found != None:

        ClaseDB.DeleteQueue(found['Id'])

        #! CLASH
        nivel = ClaseDB.GetLevel(prestigio1, prestigio2)
        actividad = ClaseDB.GenerateActivity(nivel)
        preguntas = actividad['Preguntas']
        respuestas = actividad['Respuestas']
    
    else:
        ClaseDB.AddQueue(_id, user['Prestigio'])

@app.route('/hasmatch/<int:_id>', methods=['GET'])
def hasmatch(_id):

    inQueue = ClaseDB.InQueue(_id)

    if inQueue:
        return jsonify({
            "message": "Waiting"
        }), 200
    
    else:
        partida = ClaseDB.FindGame(_id)

        if partida:

            return jsonify({
                "partida": partida
            }), 200
        
        else:
            return jsonify({
                "message": "Juego cancelado"
            }), 400


if __name__ == '__main__':
    app.run(debug=True)