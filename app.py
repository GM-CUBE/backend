from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS
from dotenv import load_dotenv
import os, random
from datetime import datetime
from openai import OpenAI

from my_lib.general import crud_template, is_none
from my_lib.database import DB_interface, Queue, User, Games, Questions, Clash, Game_Question, Shortcuts, Shortcut_Game, Clash_Question, Level, Paragraph, Example

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
        token = create_access_token(identity=register.Username)

        return jsonify({
            "message": "Created Successfully",
            "user": register.serialize(),
            "token": token
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
@jwt_required()
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
        if queue.Prestige >= user.Prestige - 20 and queue.Prestige <= user.Prestige + 20 and queue.IdUser != user.Id:
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
            "match": clash.serialize(),
            "game": game_player1.serialize()
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

        matches: list[Clash]  = database.read_all_table('clash')
        match = [match for match in matches if match.Game2_id == game.Id][0]

        clash_questions: list[Clash_Question] = database.read_all_table('clash_questions')
        clash_questions = [question for question in clash_questions if question.Clash_Id == match.Id]

        questions = []
        for question in clash_questions:
            q = database.read_by_id('questions', question.Question_Id)
            questions.append(q)

        return jsonify({
            "message": "Match Found",
            "game": game.serialize(),
            "match": match.serialize(),
            "questions": [question.serialize() for question in questions]
        }), 200


@app.route(URI + '/game_over/<int:clash_id>', methods=['PUT'])
@crud_template(request, optional_fields=['game_id'])
# @jwt_required()
def game_over(clash_id):
    clash: Clash = database.read_by_id('clash', clash_id)

    if clash.Game1_id == request.json['game_id']:
        database.update_table_row('clash', clash_id, {
            'EndTime': datetime.now(),
            'Result': False
        })

    elif clash.Game2_id == request.json['game_id']:
        database.update_table_row('clash', clash_id, {
            'EndTime': datetime.now(),
            'Result': True
        })

    else:
        return jsonify({
            "message": "Invalid game"
        }), 400
    
    return jsonify({
        "message": "Game ended successfully"
    }), 200


@app.route(URI + '/should_continue/<int:clash_id>/<int:game_id>', methods=['GET'])
@jwt_required()
def should_continue(clash_id, game_id):
    clash: Clash = database.read_by_id('clash', clash_id)

    if is_none(clash):
        return jsonify({
            "message": "Clash not found"
        }), 404

    opponent_game_id = ''

    if clash.Game1_id == game_id:
        opponent_game_id = clash.Game2_id

    elif clash.Game2_id == game_id:
        opponent_game_id = clash.Game1_id

    else:
        return jsonify({
            "message": "Invalid game"
        }), 400
    
    opponent_game: Games = database.read_by_id('games', opponent_game_id)

    game_questions: list[Game_Question] = database.read_all_table('game_question')

    opponent_questions = [game_quest for game_quest in game_questions if game_quest.Game_id == opponent_game.Id]

    my_questions = [game_quest for game_quest in game_questions if game_quest.Game_id == game_id]

    if len(my_questions) > len(opponent_questions):
        return jsonify({
            "state": 1,
            "message": "Waiting for opponent"
        }), 200

    else:
        has_wrong = len([game_quest for game_quest in opponent_questions if game_quest.Result == False]) != 0

        if has_wrong:
            return jsonify({
                "state": 2,
                "message": "You Won"
            }), 200
        else:  
            if len(my_questions) == 5:
                my_time, opponent_time = 0

                for i in range(len(my_questions)):
                    my_time += my_questions[i].Time
                    opponent_time += opponent_questions[i].Time

                if my_time < opponent_time:
                    return jsonify({
                        "state": 2,
                        "message": "You Won"
                    }), 200
                else:    
                    return jsonify({
                        "state": 3,
                        "message": "You Lost"
                    }), 200

            else:
                return jsonify({
                    "state": 0,
                    "message": "Must Continue"
                }), 200


@app.route(URI + 'shortcut', methods=['GET'])
@app.route(URI + 'shortcut/<int:game_id>', methods=['POST', 'GET'])
@crud_template(request, ['shortcut'])
@jwt_required()
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
        
        user: User = database.read_by_id('user', game.User_id)

        database.update_table_row('user', user.Id, {
            "Coins": user.Coins - shortcut.Price
        })
        
        _, register = database.crate_table_row('shortcut_game', {
            "IdShortcut": shortcut.Id,
            "Game_id": game.Id
        })

        return jsonify({
            "message": f"Shortcut: {shortcut.Name} used",
            "register": register.serialize()
        }), 201


@app.route(URI + 'answer/<int:_idGame>/<int:_idQuestion>', methods=['POST'])
@crud_template(request, ['Time', 'Answer'])
@jwt_required()
def answer(_idGame, _idQuestion):

    time = request.json['Time']
    answer = request.json['Answer']
    
    question: Questions = database.read_by_id('questions', _idQuestion)
    
    if not is_none(question):
        text =f"Solo dime 'verdadero' o 'falso', sin explicaciones, si la respuesta es correcta. \nEjercicio: {question.Question}\nRespuesta: {answer}"
        
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
            "Answer": str(answer),
            "Time": time,
            "Result": True if "verdadero" in completion.choices[0].message.content.lower() else False,
            "Question": question.Id,
            "Game_id": _idGame
        }

        _, register = database.crate_table_row('game_question', g_q)

        return jsonify({
            "respuesta": register.Result
        }), 200

    return jsonify({
        "message": "Unexistent Data"
    }), 404


@app.route(URI + 'lesson/<int:_idUser>', methods=['GET'])
@jwt_required()
def lesson(_idUser):
    user: User = database.read_by_id('user', _idUser)

    if not is_none(user):

        level = database.read_level(user.Prestige)
        
        if not is_none(level):

            lessons: list[Paragraph] = database.read_all_table('paragraph')
            print(lessons)

            paragraphs = [p for p in lessons if p.Level_id <= level.Id]
            
            examples_list: list[Example] = database.read_all_table('example')

            examples = [e for e in examples_list if e.Level_id <= level.Id]

            return jsonify({
                "paragraph": [p.serialize() for p in paragraphs],
                "example": [e.serialize() for e in examples]
            }), 200

    return jsonify({
        "message": "Unexistent Data"
    }), 404


@app.route(URI + 'levels', methods=['GET'])
@app.route(URI + 'levels/<int:idLevel>', methods=['GET'])
@jwt_required()
def getLevel(_idLevel = None):

    levels = None

    if is_none(_idLevel):

        levels: list[Level] = database.read_all_table('level')

        return jsonify({
            "levels": [level.serialize() for level in levels]
        }), 200

    else:
        level: Level = database.read_by_id(_idLevel)

        if not is_none(level):
            return jsonify({
                "level": level.serialize()
            }), 200
        
    return jsonify({
        "message": "DATA NOT FOUND"
    }), 404


@app.route(URI + 'me/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
@crud_template(request, optional_fields=["FirstName", "LastName", "Age", "Username", "Streak", "Coins", "Prestige"])
@jwt_required()
def me(user_id):
    user: User = database.read_by_id('user', user_id)

    if is_none(user):
        return jsonify({
            "message": "User not found"
        }), 404
    
    if request.method == "GET":
        return jsonify({
            "user": user.serialize()
        }), 200
    
    elif request.method == "PUT":
        database.update_table_row('user', user_id, request.json)
        
        return jsonify({
            "message": "Info Updated"
        }), 200
    
    elif request.method == "DELETE":
        database.delete_table_row('user', user_id)
        
        return jsonify({
            "message": "Your were deleted"
        }), 200

if __name__ == '__main__':
    app.run(debug=True)