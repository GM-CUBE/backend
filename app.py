from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS
from dotenv import load_dotenv
import os, re, random
from hashlib import md5

from my_lib.general import crud_template, is_none
from my_lib.database import DB_interface, Queue, User, Games, Questions, Clash, Game_Question, Shortcuts, Shortcut_Game, Clash_Question

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


@app.route(URI + 'history/<int:user_id>', methods=['GET'])
def history(user_id):
    user: User = database.read_by_id('user', user_id)

    if is_none(user):
        return jsonify({
            "message": "User Not Found",
        }), 404
    
    games: list[Games] = database.read_all_table('games')

    games = [game for game in games if game.User_id == user.Id]

    matches: list[Clash]  = database.read_all_table('clash')
    games_questions: list[Game_Question] = database.read_all_table('game_question')
    games_shortcuts: list[Game_Question] = database.read_all_table('shortcut_game')

    history = []
    for game in games:
        match = [match for match in matches if match.Game1_id == game.Id or match.Game2_id == game.Id][0]
        game_questions = [gquest for gquest in games_questions if gquest.Game_id == game.Id]
        game_shortcuts = [shortcut for shortcut in games_shortcuts if shortcut.Game_id == game.Id]

        history.append({
            "info": game.serialize(),
            "match": match.serialize(),
            "game_questions": [gquest.serialize() for gquest in game_questions],
            "game_questions": [shortcut.serialize() for shortcut in game_shortcuts]
        })
        
    return jsonify({
        "history": history
    }), 200
    
@app.route(URI + 'queue/<int:user_id>', methods=['POST'])
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

        _, game_player1 = database.crate_table_row('games', {
            'User_id': user.Id
        })

        _, game_player2 = database.crate_table_row('games', {
            'User_id': match.IdUser
        })

        database.delete_table_row('queue', match.Id)

        level = database.read_level(min(user.Prestige, match.Prestige))

        questions: list[Questions] = database.read_all_table('questions')

        questions = [question for question in questions if question.Level_id == level.Id]

        questions = random.sample(questions, 5)

        _, clash = database.crate_table_row('clash', {
            "Level_id": level.Id,
            "Game1_id": game_player1.Id,
            "Game2_id": game_player2.Id,
        })

        for question in questions:
            database.crate_table_row('clash_questions', {
                "Clash_Id": clash.Id,
                "Question_Id": question.Id
            })

        return jsonify({
            "message": "Match Found",
            "questions": [question.serialize() for question in questions],
            "clash": clash.serialize()
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

        matches: list[Clash]  = database.read_all_table('clash')
        match = [match for match in matches if match.Game2_id == game.Id][0]

        clash_questions: list[Clash_Question] = database.read_all_table('clash_questions')
        clash_questions = [question for question in clash_questions if question.Clash_Id == match.Id]

        return jsonify({
            "game": game.serialize(),
            "match": match.serialize(),
            "questions": [question.serialize() for question in clash_questions]
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


@app.route(URI + 'shortcut', methods=['GET'])
@app.route(URI + 'shortcut/<int:game_id>', methods=['POST', 'GET'])
@crud_template(request, ['shortcut'])
def shortcut(game_id=None):

    if request.method == "GET":
        
        if is_none(game_id):
            shortcuts: list[Shortcuts] = database.read_all_table('shortcuts')
            
            return jsonify({
                "data": [shortcut.serialize() for shortcut in shortcuts]
            }), 200
        
        else:
            game: Games = database.read_by_id('games', game_id)
            
            if is_none(game):
                return jsonify({
                    "message": "Unexistent Data" 
                }), 404
            
            shortcuts: list[Shortcut_Game] = database.read_all_table('shortcut_game')
            shortcuts = [shortcut for shortcut in shortcuts if shortcut.Game_id == game.Id]

            return jsonify({
                "message": "Used Shortcuts",
                "data": [shortcut.serialize() for shortcut in shortcuts]
            }), 200


    elif request.method == "POST":
        shortcut_id = request.json['Shortcut']
        
        shortcut: Shortcuts = database.read_by_id('shortcuts', shortcut_id)
        game: Games = database.read_by_id('games', game_id)

        if is_none(shortcut) or is_none(game):
            return jsonify({
                "message": "Unexistent Data" 
            }), 404
        
        _, register = database.crate_table_row('shortcut_game', {
            "IdShortcut": shortcut.Id,
            "Game_id": game.Id
        })

        return jsonify({
            "message": f"Shortcut: {shortcut.Name} used",
            "register": register.serialize()
        }), 201


# @app.route(URI + 'answer/<int: _idGame>/<int: _idQuestion>', methods=['POST'])
# @crud_template(request, ['Time', 'Answer'])
# def answer(_idGame, _idQuestion):

#     time = request.json['Time']
#     answer = request.json['Answer']

#     #todo validacion de respuesta

#     regex = ClaseDB.GetAnswer(_idQuestion)

#     result = re.search(regex, answer)

#     if result:
#         isCorrect = True
#     else:
#         isCorrect = False

#     ClaseDB.AddAnswer(_idQuestion, _idGame, time, answer, isCorrect)


if __name__ == '__main__':
    app.run(debug=True)