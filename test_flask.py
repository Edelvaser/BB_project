from flask import Flask, jsonify, request
import json
from model import User, Quiz
from work_bd import LearningBD
from dop_function import check_email, check_password
import time
from allData import subject

app = Flask(__name__)
bd = LearningBD()

@app.get("/")
def index():
    return jsonify("Ok")

@app.get("/ping/")
def pong():
    return jsonify("pong")

@app.post("/reg/")
def reg():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = json.loads(request.data)
        if not check_email(data["login"]):
            return jsonify({"error":"Login incorrect"})
        elif not check_password(data["password"]):
            return jsonify({"error":"Password incorrect"})
        elif data["password"] != data["rep_pass"]:
            return jsonify({"error":"Passwords don't match"})
        elif not bd.check_free_login(data["login"]):
            return jsonify({"error":"Login occupied"})
        else:
            user = User(data["login"], data["password"])
            bd.add_user(user)
            return jsonify({'token':user.token})
    else:
        return 'Content-Type not supported!'
    
@app.post("/auth/")
def auth():
    token = request.headers.get('Authorization')
    content_type = request.headers.get('Content-Type')
    if token:
        if bd.check_user_by_token(token):
            return jsonify({'token':token})
        else:
            return jsonify({'error':"Error auth"})
    elif (content_type == 'application/json'):
        data = json.loads(request.data)
        user = User(data["login"], data["password"])
        if bd.check_user_by_login(user):
            return jsonify({'token':user.token})
        else:
            return jsonify({"error":"Error auth"})
    else:
        return 'Content-Type not supported!'

@app.post("/count/")
def count_num():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = json.loads(request.data)
        data["aaa"] += 1
        data["bbb"] += 2
        return jsonify(data)
    else:
        return 'Content-Type not supported!'

@app.post("/check_team/")
def check_team():
    token = request.headers.get('Authorization')
    content_type = request.headers.get('Content-Type')
    if token and content_type == 'application/json' and bd.check_user_by_token(token):
        _, id_user = bd.get_user_by_token(token)
        data = json.loads(request.data)
        print("id_user", id_user)
        if "id_team" in data:
            pos, status = bd.check_team(data['id_team'], id_user)
            print(pos)
            if status: return jsonify({"error":"Игра окончена"}) # Game over
            elif pos == 0: return jsonify({"error":"Команда заполнена"}) # Team is full
            elif pos == -1: return jsonify({"Ok":"Вы уже в команде"}) # User already in team
            elif pos == -2: return jsonify({"error":"Команда не найдена"}) #Not teams
            elif pos not in (2, 3): return jsonify({"error":"Error DB"})
            else: return jsonify({"Ok":"User added in team"})
        else:
            return jsonify({"error":"Error data"})
    else:
        return jsonify({"error":"Not auth"})

@app.post("/create_team/")
def create_team():
    token = request.headers.get('Authorization')
    content_type = request.headers.get('Content-Type')
    if token and content_type == 'application/json' and bd.check_user_by_token(token):
        data = json.loads(request.data)
        _, id_user = bd.get_user_by_token(token)
        id_team = bd.create_team(id_user, data["name"])
        if not id_team:
            return jsonify({"error":"Error create team"})
        return jsonify({'id_team':id_team})
    else:
        return jsonify({"error":"Not auth"})

@app.post("/set_ready/")
def set_ready():
    token = request.headers.get('Authorization')
    content_type = request.headers.get('Content-Type')
    if token and content_type == 'application/json' and bd.check_user_by_token(token):
        _, id_user = bd.get_user_by_token(token)
        data = json.loads(request.data)
        id_team = data["team"]
        if "subject" in data and data["subject"]:
            id_subj = subject.index(data["subject"]) + 1
        else:
            id_subj = bd.get_id_subject(id_team)
        print("Id_subject", id_subj)
        ready = bd.set_ready(id_team, id_user, data["ready"])
        if not ready:
            return jsonify({"wait":"Wait"})
        len_team = bd.get_len_team(id_team)
        if len_team:
            quiz = bd.create_quiz(id_subj, id_team, len_team*2)
            quiz_json = quiz.make_json()
            quiz_json["Ok"] = "Ok"
            return jsonify(quiz_json)
        return jsonify({'Error':"error bd"})
    else:
        return jsonify({"error":"Not auth"})

@app.post("/check_answer/")
def check_answer():
    token = request.headers.get('Authorization')
    content_type = request.headers.get('Content-Type')
    if token and content_type == 'application/json' and bd.check_user_by_token(token):
        _, id_user = bd.get_user_by_token(token)
        data = json.loads(request.data)
        id_team = data["id_team"]
        if "subject" in data and data["subject"]:
            id_subj = subject.index(data["subject"]) + 1
        else:
            id_subj = bd.get_id_subject(id_team)
        print(data)
# data = {"answer":answer, "id_quest":id_que, "subject":self.id_subject, "id_team":self.id_team}
        ready = bd.check_answer(data["answer"], data["id_quest"], id_user, id_team)
        if ready == -1:
            return jsonify({"error":"Not game"})
        elif ready == 0:
            return jsonify({"error":"Game over"})
        else:
            return jsonify({"ok":"answer added"})
    else:
        return jsonify({"error":"Not auth"})

@app.post("/check_status_game/")
def check_status_game():
    token = request.headers.get('Authorization')
    content_type = request.headers.get('Content-Type')
    if token and content_type == 'application/json' and bd.check_user_by_token(token):
        _, id_user = bd.get_user_by_token(token)
        data = json.loads(request.data)
        id_team = data["id_team"]; count_que = data["count_que"]
        print(data)
        ready = bd.check_status_game(id_team, count_que)
        return jsonify({"status":ready})
    else:
        return jsonify({"error":"Not auth"})


@app.post("/reset_result/")
def reset_result():
    token = request.headers.get('Authorization')
    content_type = request.headers.get('Content-Type')
    if token and content_type == 'application/json' and bd.check_user_by_token(token):
        _, id_user = bd.get_user_by_token(token)
        data = json.loads(request.data)
        id_team = data["id_team"]
        ready = bd.check_result(id_team)
        print("ready:", ready)
        if ready>=0:
            bd.set_game_over(id_user, id_team)
        return jsonify({"ok":ready})
    else:
        return jsonify({"error":"Not auth"})


@app.post("/set_game_over/")
def set_game_over():
    token = request.headers.get('Authorization')
    content_type = request.headers.get('Content-Type')
    if token and content_type == 'application/json' and bd.check_user_by_token(token):
        _, id_user = bd.get_user_by_token(token)
        data = json.loads(request.data)
        id_team = data["id_team"]
        res = bd.set_game_over(id_user, id_team)
        if res:
            return jsonify({"ok":"Game over"})
        else:
            return jsonify({"error":"Not your game"})
    else:
        return jsonify({"error":"Not auth"})



if __name__ == "__main__":
    app.run(debug=True)