import psycopg2

import os
from model import User, Quiz
import datetime
import time
import random
from allData import *

class LearningBD():
    def __init__(self, dbname='learning', user='postgres', password=os.getenv('pgmp')):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.make_table()
        self.add_data()

    def connect_to_db(self):
        conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password)
        cur = conn.cursor()
        return conn, cur
    # "CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);"

    def make_table(self):
        conn, cur = self.connect_to_db()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
            id_user serial PRIMARY KEY,
            login TEXT,
            password TEXT,
            rating INTEGER,
            token TEXT,
            date bigint
            );
        """)

        cur.execute("""CREATE TABLE IF NOT EXISTS game(
            id_team serial PRIMARY KEY,
            id_user_a integer,
            id_user_b integer,
            id_user_c integer,
            id_rddm_subj integer,
            status bool
            );
        """)

        cur.execute("""CREATE TABLE IF NOT EXISTS round(
            id serial PRIMARY KEY,
            id_team integer,
            id_user integer,
            ready bool,
            all_q integer,
            right_q text
            );
        """)

        cur.execute("""CREATE TABLE IF NOT EXISTS rddm_subject(
            id serial PRIMARY KEY,
            name text
            );
        """)

        cur.execute("""CREATE TABLE IF NOT EXISTS rddm_question(
            id serial PRIMARY KEY,
            id_subject int,
            quest text
            );
        """)

        cur.execute("""CREATE TABLE IF NOT EXISTS rddm_answers(
            id serial PRIMARY KEY,
            id_quest int,
            answer text
            );
        """)
        conn.commit()
        cur.close()
        conn.close()

    def add_rddm_subject(self, name):
        conn, cur = self.connect_to_db()
        cur.execute("INSERT INTO rddm_subject (name) VALUES (%s)", name)
        conn.commit()
        cur.close()
        conn.close()

    def add_all_rddm_subjects(self, subj):
        conn, cur = self.connect_to_db()
        for s in subj:
            cur.execute("INSERT INTO rddm_subject (name) VALUES (%s);", (s,))
        conn.commit()
        cur.close()
        conn.close()

    def add_rddm_question(self, id_sub, quest, answer):
        conn, cur = self.connect_to_db()
        cur.execute("""INSERT INTO rddm_question (id_subject, quest) VALUES (%s, %s)
       ;""", (id_sub, quest))
        # RETURNING id;""", (id_sub, quest))
        cur.execute("""SELECT LAST_INSERT_ID();""")
        res = cur.fetchone()
        if res:
            for a in answer:
                cur.execute("""INSERT INTO rddm_answers (id_quest, answer) VALUES (%s, %s)""", (res[0], a))
        conn.commit()
        cur.close()
        conn.close()

    def add_all_rddm_question(self, questions, answers):
        conn, cur = self.connect_to_db()
        id_subj = []
        for i in range(len(questions)):
            cur.execute("""INSERT INTO rddm_question (id_subject, quest) VALUES (%s, %s) 
                ;""", (questions[i][0], questions[i][1]))
                # RETURNING id;""", (questions[i][0], questions[i][1]))
            cur.execute("""SELECT LAST_INSERT_ID();""")
            res = cur.fetchone()
            if res:
                for a in answers[i]:
                    cur.execute("""INSERT INTO rddm_answers (id_quest, answer) VALUES (%s, %s);""", (res[0], a))
        conn.commit()
        cur.close()
        conn.close()
        return id_subj

    def add_data(self):
        conn, cur = self.connect_to_db()
        cur.execute("SELECT count(id) from rddm_subject;")
        res = cur.fetchone()[0]
        if res == 0:
            self.add_all_rddm_subjects(subject)
        

        cur.execute("SELECT count(id) from rddm_question;")
        res = cur.fetchone()[0]
        if res == 0:
            self.add_all_rddm_question(quest, answers)
        conn.commit()
        cur.close()
        conn.close()

    def add_user(self, user):
        try:
            conn, cur = self.connect_to_db()
            req = """SELECT login FROM users 
            WHERE login = %s; """
            cur.execute(req, (user.login,))
            res = cur.fetchone()
            # print(res)
            if not res:
                cur.execute("INSERT INTO users(login, password, rating,\
                            token, date)\
                                VALUES(%s, %s, %s, %s, %s);", \
                            (user.login, user.passw, user.rating,
                            user.token, user.date))
                conn.commit()
            return True
        except:
            cur.close()
            conn.close()
            return False

    def get_user_id(self, login):
        try:
            conn, cur = self.connect_to_db()
            req = """SELECT id_user FROM users 
            WHERE login = %s; """
            cur.execute(req, (login,))
            res = cur.fetchone()
            cur.close()
            conn.close()
            return res[0]
        except:
            cur.close()
            conn.close()
            return 0

    def update_user(self, user):
        try:
            conn, cur = self.connect_to_db()
            id = self.get_user_id(user.login)
            cur.execute("""UPDATE users SET rating=%s, token=%s, date=%s
                            WHERE id_user=%s;""", 
                            (user.rating, user.token, user.date, id))
            conn.commit()
            return True
        except:
            cur.close()
            conn.close()
            return False

    def get_user_by_login(self, login):
        conn, cur = self.connect_to_db()
        cur.execute("""SELECT * FROM users
                    WHERE login = %s;""", (login,))
        res = cur.fetchone()
        cur.close()
        conn.close()
        if res is not None:
            user = User(res[1], res[2])
            user.set_user_bd(res[3], res[4], res[5])
            return user
        else:
            return res
    
    def get_user_by_token(self, token):
        conn, cur = self.connect_to_db()
        cur.execute("""SELECT * FROM users
                    WHERE token = %s;""", (token,))
        res = cur.fetchone()
        cur.close()
        conn.close()
        if res is not None:
            user = User(res[1], res[2])
            user.set_user_bd(res[3], res[4], res[5])
            return user, res[0]
        else:
            return res, None

    def check_user_by_login(self, user):
        conn, cur = self.connect_to_db()
        cur.execute("""SELECT login, password FROM users
                    WHERE login = %s;""", (user.login,))
        res = cur.fetchone()
        if res and user.passw == res[1]:
            cur.execute("""UPDATE users SET token=%s
                    WHERE login = %s;""", (user.token, user.login))
            conn.commit()
            cur.close()
            conn.close()
            return True
        else:
            cur.close()
            conn.close()
            return False
        
    def check_user_by_token(self, token):
        conn, cur = self.connect_to_db()
        cur.execute("""SELECT date FROM users
                    WHERE token = %s;""", (token,))
        res = cur.fetchone()
        cur.close()
        conn.close()
        if not res: return res
        date_token = datetime.datetime.fromtimestamp(res[0])
        date = datetime.datetime.now()
        if res and (date_token - date).days > 0:
            return True
        else:
            return False

    def check_free_login(self, login):
        conn, cur = self.connect_to_db()
        cur.execute("""SELECT * FROM users
                    WHERE login = %s;""", (login,))
        res = cur.fetchone()
        cur.close()
        conn.close()
        if res:
            return False
        else:
            return True

    def boom(self):
        conn, cur = self.connect_to_db()
        cur.execute("DROP TABLE IF EXISTS users;")
        cur.execute("DROP TABLE IF EXISTS game;")
        cur.execute("DROP TABLE IF EXISTS round;")
        cur.execute("DROP TABLE IF EXISTS rddm_answers;")
        cur.execute("DROP TABLE IF EXISTS rddm_question;")
        cur.execute("DROP TABLE IF EXISTS rddm_subject;")

        conn.commit()
        cur.close()
        conn.close()

        # id_team integer PRIMARY KEY,
        # user_a_ready bool,
        # user_b_ready bool,
        # user_c_ready bool,
        # game bool

    def create_team(self, id_user_a, name_rddm):
        conn, cur = self.connect_to_db()
        cur.execute("""SELECT id from rddm_subject WHERE name=%s;""",(name_rddm,))
        id_rddm_subj = cur.fetchone()[0]
        print(id_rddm_subj)
        if not id_rddm_subj: return None
        cur.execute("""INSERT INTO game (status, id_rddm_subj)
        VALUES(%s, %s) 
        ;""", (False, id_rddm_subj))
        # RETURNING id_team;""", (False, id_rddm_subj))
        cur.execute("""SELECT LAST_INSERT_ID();""")
        res = cur.fetchone()
        if not res: return None
        id_team = res[0]
        cur.execute("""INSERT INTO round (id_team, id_user, ready, all_q, right_q)
        VALUES(%s, %s, %s,%s,%s);""", (id_team, id_user_a, False,0 ,""))
        # VALUES(%s, %s, %s,%s,%s) RETURNING id;""", (id_team, id_user_a, False,0 ,""))
        cur.execute("""SELECT LAST_INSERT_ID();""")
        res = cur.fetchone()[0]
        print("id_team",res)
        if not res: return None
        cur.execute("""UPDATE game SET id_user_a=%s WHERE id_team=%s""",\
                    (res, id_team))
        conn.commit()
        cur.close()
        conn.close()
        return id_team

    def check_team(self, id_team, id_user):
        """ returns 0 - full team, -1 - user already in team, 2 or 3 - place user in team -2 - not team
        """
        conn, cur = self.connect_to_db()
        cur.execute("""SELECT * FROM game 
            WHERE id_team=%s;""", (id_team,))
        team = cur.fetchone()
        # if team[4] == True:
        #     return
        cur.execute("""SELECT id_user FROM round WHERE id_team=%s;""", (id_team,))
        res = [a[0] for a in cur.fetchall()]
        print(res)
        if len(res) == 0:
            return -2, False
        if id_user in res:
            return -1, team[5]
        if len(res) == 1:
            cur.execute("""INSERT INTO round (id_team, id_user, ready, all_q, right_q)
                VALUES(%s, %s, %s,%s,%s);""", (id_team, id_user,False,0,""))
                # VALUES(%s, %s, %s,%s,%s) RETURNING id;""", (id_team, id_user,False,0,""))      
            cur.execute("""SELECT LAST_INSERT_ID();""")
            id_round = cur.fetchone()[0]
            cur.execute("""UPDATE game SET id_user_b=%s WHERE id_team=%s""",(id_round, id_team))
            pos = 2
        elif len(res) == 2:
            cur.execute("""INSERT INTO round (id_team, id_user, ready, all_q, right_q)
                VALUES(%s, %s, %s,%s,%s) ;""", (id_team, id_user,False,0,""))
                # VALUES(%s, %s, %s,%s,%s) RETURNING id;""", (id_team, id_user,False,0,""))
            cur.execute("""SELECT LAST_INSERT_ID();""")
            id_round = cur.fetchone()[0]
            cur.execute("""UPDATE game SET id_user_c=%s WHERE id_team=%s""",(id_round,id_team))
            pos = 3
        else:
            return 0, team[5]
        conn.commit()
        cur.close()
        conn.close()
        return pos, team[5]

    def set_ready(self, id_team, id_user, bool_ready):
        conn, cur = self.connect_to_db()
        cur.execute("""SELECT id, ready FROM round WHERE id_team=%s AND id_user=%s;""",(id_team,id_user))
        id_round, ready = cur.fetchone()
        cur.execute("""UPDATE round SET ready=%s WHERE id=%s;""", (bool_ready, id_round))
        conn.commit()
        res = self.__check_all_ready(conn, cur, id_team)
        cur.close()
        conn.close()
        return res

    def __check_all_ready(self, conn, cur, id_team):
        cur.execute("""SELECT ready FROM round WHERE id_team=%s;""",(id_team,))
        ready = cur.fetchall()[0]
        ans = True
        for a in ready:
            ans *= a
        return ans

    def check_select(self, select):
        conn, cur = self.connect_to_db()
        cur.execute(select)
        res = cur.fetchall()
        cur.close()
        conn.close()
        return res

    def get_len_team(self, id_team):
        conn, cur = self.connect_to_db()
        cur.execute("SELECT count(id_user) from round WHERE id_team=%s;", (id_team,))
        res = cur.fetchone()
        cur.close()
        conn.close()
        if res:
            return res[0]
        else:
            return 0
        
    def get_id_subject(self, id_team):
        conn, cur = self.connect_to_db()
        cur.execute("SELECT id_rddm_subj FROM game WHERE id_team=%s", (id_team, ))
        res = cur.fetchone()
        cur.close()
        conn.close()

        if res:
            return res[0]
        else:
            return res

    def create_quiz(self, id_subj, id_team, count = 4):
        conn, cur = self.connect_to_db()
        cur.execute("SELECT id, quest FROM rddm_question WHERE id_subject=%s;", (id_subj, ))
        res = cur.fetchall()
        list_quiz = random.sample(res, k = count)
        # ans = []
        # for q in list_quiz:
        #     cur.execute("SELECT answer FROM rddm_answers WHERE id_quest=%s;", (q[0], ))
        #     res = cur.fetchall()
        #     ans.append([a[0] for a in res])
        # cur.execute("""UPDATE round SET all_q=%s WHERE id_team=%s;""", (count, id_team))
        # conn.commit()
        quiz = Quiz(id_subj, count)
        quiz.add_quest(list_quiz)
        cur.close()
        conn.close()
        return quiz

    def check_answer(self, answer, id_que, id_user, id_team):
        game_status = self.get_game_status(id_team)
        if game_status is None:
            return -1
        elif game_status:
            return 0
        conn, cur = self.connect_to_db()
        cur.execute("SELECT answer FROM rddm_answers where id_quest=%s;", (int(id_que),))
        res = cur.fetchall()
        if res:
            answ = [aa[0] for aa in res]
            cur.execute("SELECT all_q, right_q FROM round WHERE id_team=%s AND id_user=%s", (id_team, id_user))
            ans_all, right_all = cur.fetchone()
            print(ans_all, right_all)
            for a in answ:
                if a.lower() == answer.lower():
                    ####
                    right_all += "1"
                    break
            else:
                right_all += "0"
            cur.execute("UPDATE round SET all_q=%s, right_q=%s WHERE id_team=%s AND id_user=%s", 
                                    (ans_all+1, right_all, id_team, id_user))
            conn.commit()
            cur.close()
            conn.close()
            return 1
        else:
            return None

    def get_game_status(self, id_team):
        conn, cur = self.connect_to_db()
        cur.execute("SELECT status FROM game WHERE id_team=%s", (id_team, ))
        res = cur.fetchone()
        cur.close()
        conn.close()
        if res:
            return res[0]
        return res

    def set_game_over(self, id_user, id_team):
        conn, cur = self.connect_to_db()
        # cur.execute("SELECT id_user_a, id_user_b, id_user_c FROM game WHERE id_team=%s",(id_team,))
        # res0 = cur.fetchall()
        # cur.execute("SELECT id FROM round WHERE id_team=%s",(id_team,))
        # res1 = cur.fetchall()
        # if res0 and res1:
        #     rounds = [a[0] for a in res0]
        #     users = [a[0] for a in res1]
            # if id_user in users:
        cur.execute("UPDATE game SET status=%s WHERE id_team=%s", (True, id_team))
        conn.commit()
            #     result = True
            # else:
            #     result = False
        cur.close()
        conn.close()
        # return result

    def check_status_game(self, id_team, count_que):
        conn, cur = self.connect_to_db()
        cur.execute("""SELECT right_q FROM round
                WHERE id_team=%s
                GROUP BY id_team, right_q;
        """, (id_team, ))
        res = cur.fetchall()
        ready = True
        cur.close()
        conn.close()
        if res:
            rea = [a[0] for a in res]
            for a in rea:
                ready *= len(a)==count_que
            return ready
        else:
            return False

    def check_result(self, id_team):
        conn, cur = self.connect_to_db()
        cur.execute("""SELECT right_q FROM round WHERE id_team=%s AND ready=true;""", (id_team, ))
        res = cur.fetchall()
        cur.close()
        conn.close()
        print(res)
        if res:
            ready = len(res[0][0])*"0"
            for a in res:
                ready = bin(int(ready,2)| int(a[0],2))
            return ready[2:].count("1")
        else:
            return -1
