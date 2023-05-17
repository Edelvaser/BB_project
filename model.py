import datetime
import json
from hashlib import sha256
import os

class User():
    def __init__(self, login, passw):
        self.login = login
        self.passw = sha256((login+passw).encode()).hexdigest()
        self.rating = 0
        self.date = int((datetime.datetime.now() + datetime.timedelta(days=30)).timestamp())
        self.token = sha256((login+passw + os.getenv("tokenSalt") + str(self.date))\
                .encode()).hexdigest()

    def set_user_bd(self, rating, token, date):
        self.rating = rating
        self.token = token
        self.date = date

    def new_token(self):
        self.date = int((datetime.datetime.now() + datetime.timedelta(days=30)).timestamp())
        self.token = sha256((self.login+self.passw + os.getenv("tokenSalt") \
                + str(self.date)).encode()).hexdigest()

    def json_user(self):
        return json.dumps(self.__dict__)
    
    def set_rating(self):
        self.rating += 1

class Quest():
    def __init__(self, id_quest, quest) -> None:
        self.id_quest = id_quest
        self.quest = quest
        # self.answ = answ

class Quiz():
    def __init__(self, id_subject, count_quest):
        self.id_subject = id_subject
        self.count_quest = count_quest
        self.quests = []
    
    # def add_quest(self, list_quiz, ans):
    #     for q in range(len(list_quiz)):
    #         quest = Quest(list_quiz[q][0], list_quiz[q][1], ans[q])
    #         self.quests.append(quest)

    def add_quest(self, list_quiz):
        for q in range(len(list_quiz)):
            quest = Quest(list_quiz[q][0], list_quiz[q][1])
            self.quests.append(quest)
    
    
    def make_json(self):
        res = {"id_subject": self.id_subject, "count_quest":self.count_quest}
        res["quests"] = []
        for q in self.quests:
            que = {}
            que["id_quest"] = q.id_quest
            que["quest"] = q.quest
            res["quests"].append(que)
        return res


class Game():
    def __init__(self, id_team, id_subject, count_user):
        self.id_team = id_team
        self.id_subject = id_subject
        self.count_user = count_user




# u = User("aaa", "111")
# print(u.json_user())
