from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS
from dotenv import load_dotenv
import os, random
from openai import OpenAI

from my_lib.general import crud_template, is_none
from my_lib.database import DB_interface, Queue, User, Games, Questions, Level, Paragraph, Example

# -----------------------------------------------------------------------------

load_dotenv()

app = Flask(__name__)
CORS(app)
JWTManager(app)
database = DB_interface()

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

URI = '/api/v1/'

# -----------------------------------------------------------------------------

@app.route(URI + 'signup', methods=['POST'])
@crud_template(request, ['firstName', 'lastName', 'age', 'username', 'password'])
def signup():
    if database.exist_user(request.json['username']):
        return jsonify({
            "message": "User already exist"
        }), 302

    created, register = database.crate_table_row(
        'user', 
        {
            'FirstName': request.json['firstName'] ,
            'LastName': request.json['lastName'], 
            'Age': request.json['age'], 
            'Username': request.json['username'],
            'Password': request.json['password'], 
        }
    )

    if created:
        return jsonify({
            "message": "Created Successfully",
            "user": register.serialize()
        }), 201
    
    return jsonify({
        "message": "Error while creating"
    }), 501


@app.route(URI + 'login', methods=['POST'])
@crud_template(request, ['username', 'password'])
def login():
    username = request.json['username']
    password = request.json['password']

    success, user = database.try_login(username, password)

    if success:
        token = create_access_token(identity=username)
        
        return jsonify({
            "message": "Login Successfully",
            "user": user.serialize(),
            "token": token
        }), 200
        
    else:
        return jsonify({
            "message": "Incorrect Credentials",
        }), 401


@app.route(URI + 'queue/<int:user_id>', methods=['POST'])
@jwt_required()
def queue(user_id):
    
    user: User = database.read_by_id('user', user_id)

    if is_none(user):
        return jsonify({
            "message": "User Not Found",
        }), 404

    queues: list[Queue] = database.read_all_table('queue')
    
    match = None

    for queue in queues:
        if queue.Prestige >= user.Prestige - 20 and queue.Prestige <= user.Prestige + 20:
            match = queue
            break

    if match != None:

        game_player1: Games = database.crate_table_row('games', {
            'User_id': user.Id
        })

        game_player2: Games = database.crate_table_row('games', {
            'User_id': match.IdUser
        })

        database.delete_table_row('queue', match.Id)

        level = database.read_level(min(user.Prestige, match.Prestige))

        questions: list[Questions] = database.read_all_table('questions')

        questions = [question for question in questions if question.Level_id == level.Id]

        # questions = random.sample(questions, 5)

        return jsonify({
            "message": "Match Found",
            "min": level.serialize(),
            "questions": [question.serialize() for question in questions]
        }), 201
    
    else:
        database.crate_table_row('queue', {
            "IdUser": user.Id,
            "Prestige": user.Prestige
        })

        queues: list[Queue] = database.read_all_table('queue')

        return jsonify({
            "message": "Waiting...",
            "queue": [queue.serialize() for queue in queues]
        }), 201


@app.route(URI + 'has_match/<int:user_id>', methods=['GET'])
@jwt_required()
def has_match(user_id):
    user: User = database.read_by_id('user', user_id)

    if is_none(user):
        return jsonify({
            "message": "User Not Found",
        }), 404

    queues: list[Queue] = database.read_all_table('queue')
    
    inQueue = False

    for queue in queues:
        if queue.IdUser == user.Id:
            inQueue = True
            break

    if inQueue:
        return jsonify({
            "message": "Waiting..."
        }), 200
    
    else:
        games: list[Games] = database.read_all_table('games')

        game = [game for game in games if game.User_id == user.Id and game.Amount == 0][0]

        return jsonify({
            "game": game.serialize()
        }), 200


# @app.route('/gameover/<int:_id>', methods=['GET', 'POST'])
# @crud_template(request, ['Prestige', 'Coins', 'Victory'])
# def juegoterminado(_id):

#     newPrestige = request.json['Prestige']
#     newCoins = request.json['Coins']
#     isVictory = request.json['Victory']

#     ClaseDB.JuegoTerminado(_id, newPrestige, newCoins, isVictory)

#     user = ClaseDB.GetUser(_id)

#     created = database.crate_table_row('user', user)

#     if created:
#         return jsonify({
#             "message": "Agregado correctamente"
#         }), 200
    
#     return jsonify({
#         "message": "No se creo la cuenta"
#     }), 501


# @app.route(URI + 'gameover/<int:_id>', methods=['GET', 'POST'])
# @crud_template(request, ['Prestige', 'Coins', 'Victory'])
# def juegoterminado(_id):

#     newPrestige = request.json['Prestige']
#     newCoins = request.json['Coins']
#     isVictory = request.json['Victory']

#     ClaseDB.JuegoTerminado(_id, newPrestige, newCoins, isVictory)

#     user = ClaseDB.GetUser(_id)

#     return jsonify({
#         "message": "Listo",
#         "user": user
#     }), 200


# @app.route(URI + 'shortcut/<int:_idgame>', methods=['POST'])
# @crud_template(request, ['Shortcut'])
# def shortcut(_idgame):

#     shortcut = request.json['Shortcut']
#     _idshort = ClaseDB.BusarShortCut(shortcut)
    
#     ClaseDB.ChangeCoins(_idgame, _idshort)
    
#     ClaseDB.Shortcut_Game(_idshort, _idgame)


# @app.route(URI + 'history/<int:_id>', methods=['GET'])
# def history(_id):
#     history = ClaseDB.History(_id)

#     return jsonify({
#         "history": history
#     }), 200


@app.route(URI + 'answer/<int:_idGame>/<int:_idQuestion>', methods=['POST'])
@crud_template(request, ['Time', 'Answer'])
@jwt_required()
def answer(_idGame, _idQuestion):

    time = request.json['Time']
    answer = request.json['Answer']
    
    questions: list[Questions] = database.read_all_table('questions')

    _question = None

    for question in questions:
        if question.Id == _idQuestion:
            _question = question
            break
    
    if not is_none(_question):
        text =f"Solo dime 'verdadero' o 'falso', sin explicaciones, si la respuesta es correcta. \nEjercicio: {_question.Question}\nRespuesta: {answer}"
        
    client = OpenAI(
        api_key=os.getenv('OPENAI_TOKEN')
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un sistema de validación de códigos de python y solo puedes responder 'verdadero' si la respuesta a los ejercicios es correcta o 'falso' si no es correcta."},
            {"role": "user", "content": text}
        ]
    )

    g_q = {
        "Answer": answer,
        "Time": time,
        "Result": True if completion.choices[0].message.content.lowe() == "verdadero" else False,
        "Question": _question.Question,
        "Game_id": _idGame
    }

    database.crate_table_row('game_question', g_q)

    return jsonify({
        "respuesta": completion.choices[0].message.content
    })


@app.route(URI + 'lesson/<int:_idUser>', methods=['GET'])
@jwt_required()
def lesson(_idUser):

    users: list[User] = database.read_all_table('users')

    user = None
    for u in users:
        if u.Id == _idUser:
            user = u
     
    if not is_none(user):

        level = database.read_level(user.Prestige)
        
        if not is_none(level):

            lessons: list[Paragraph] = database.read_all_table('paragraphs')

            paragraph = ""
            for lesson in lessons:
                if lesson.Level_id == level.Id:
                    paragraph = lesson.Information
                    break
            
            examples: list[Example] = database.read_all_table('examples')

            example = ""
            for e in examples:
                if e.Level_id == level.Id:
                    example = e.Information
                    break

            if paragraph != "" and example != "":

                return jsonify({
                    "paragraph": paragraph.serialize(),
                    "example": example.serialize()
                }), 200
    
    return jsonify({
        "message": "ERROR"
    }), 400


@app.route(URI + 'levels', methods=['GET'])
@app.rpute(URI + 'levels/<int_idLevel>', methods=['GET'])
@jwt_required()
def getLevel(_idLevel=None):

    levels = None

    if is_none(_idLevel):

        levels: list[Level] = database.read_all_table('levels')

        if len(levels) > 0:
            return jsonify({
                "levels": [level.serialize() for level in levels]
            }), 200

    else:

        level = database.read_by_id(_idLevel)

        if not is_none(level):
            return jsonify({
                "level": level.serialize()
            }), 200
        
    return jsonify({
        "message": "ERROR"
    }), 400


if __name__ == '__main__':
    app.run(debug=True)