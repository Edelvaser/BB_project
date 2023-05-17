from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from dop_function import send_request, read_token
from kivy.uix.boxlayout import BoxLayout
from kivy.base import EventLoop
import threading
import time
import random
import datetime
import asyncio

class Quiz_0(Screen):
    def bad_quiz(self, message):
        layout = GridLayout(cols = 1, padding = 10)
        popupLabel = Label(text = message, size_hint = (0.2, 0.1),
            pos_hint = {"x" : 0.3, "top" : 0.8})
        closeButton = Button(text = "Назад", size_hint = (0.2, 0.1),
                             background_normal= '', background_color= '5ED05B')
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)       
        popup = Popup(title ='Ошибка!',
                      content = layout, size_hint =(None, None), size =(200, 200))  
        popup.open()   
        closeButton.bind(on_press = popup.dismiss)  

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'start_quiz'
    
    def set_answer(self, answer, id_que):
        token = read_token()
        self.id_team = self.manager.get_screen("start_quiz").id_team
        self.id_subject = self.manager.get_screen("start_quiz").id_subject
        self.quests = self.manager.get_screen('start_quiz').quests[:]
        self.manager.get_screen("quiz0").ids.id_answer.text = ""
        try:
            self.id_que =  self.manager.get_screen("quiz1").id_que
        except:
            self.id_que = self.manager.get_screen("start_quiz").id_que
        if token:
            data = {"answer":answer, "id_quest":self.quests[self.id_que]["id_quest"], 
                    "subject":self.id_subject, "id_team":self.id_team}
            headers = {'Content-type': 'application/json',"Authorization":token}
            res = send_request(route="/check_answer/", js_obj = data, headers=headers)
            print(res)
            if "error" in res and type(res) == dict:
                self.bad_quiz(res["error"])
            elif "Error" in res:
                self.bad_quiz("Error server")
            if "ok" in res:
                self.id_que += 1
                if self.id_que < len(self.quests):
                    self.ids['id_answer'].text = ""
                    self.to_game()
                else:
                    self.id_que = 0
                    self.to_game_over()

    def to_game(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.get_screen("quiz1").ids.text_quest.text = self.quests[self.id_que]["quest"]
        # self.manager.get_screen("quiz").ids.id_quest.text = str(self.quests[0]["id_quest"])
        self.manager.current = 'quiz1'

    def to_game_over(self):
        token = read_token()
        if token:
            data = {"id_team":self.id_team, "count_que":len(self.quests)}
            headers = {'Content-type': 'application/json',"Authorization":token}
            res = send_request(route="/check_status_game/", js_obj = data, headers=headers)
            print(res)
            if "error" in res and type(res) == dict:
                self.bad_quiz(res["error"])
            elif "Error" in res:
                self.bad_quiz("Error server")
            elif "status" in res and res["status"]:
                text = "Подводим итоги..."
                # self.to_game_over()
            else:
                text = "Ожидаем других игроков"
                self.manager.get_screen("over").ids.reset.opacity = 1
                self.manager.get_screen("over").ids.reset.disabled = False
            self.manager.transition = SlideTransition(direction="right")
            self.manager.get_screen("over").ids.res.text = text
            self.manager.current = 'over'

class Quiz_1(Screen):
    def bad_quiz(self, message, title = "Ошибка!"):
        layout = GridLayout(cols = 1, padding = 10)
        popupLabel = Label(text = message, size_hint = (0.2, 0.1),
            pos_hint = {"x" : 0.3, "top" : 0.8})
        closeButton = Button(text = "Назад", size_hint = (0.2, 0.1),
                             background_normal= '', background_color= '5ED05B')
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)       
        popup = Popup(title =title,
                      content = layout, size_hint =(None, None), size =(200, 200))  
        popup.open()   
        closeButton.bind(on_press = popup.dismiss)  

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'start_quiz'
    
    def set_answer(self, answer, id_que):
        token = read_token()
        self.id_team = self.manager.get_screen("start_quiz").id_team
        self.id_subject = self.manager.get_screen("start_quiz").id_subject
        self.quests = self.manager.get_screen('start_quiz').quests[:]
        self.manager.get_screen("quiz1").ids.id_answer.text = ""
        try:
            self.id_que =  self.manager.get_screen("quiz0").id_que
        except:
            self.id_que = self.manager.get_screen("start_quiz").id_que
        if token:
            data = {"answer":answer, "id_quest":self.quests[self.id_que]["id_quest"], 
                    "subject":self.id_subject, "id_team":self.id_team}
            headers = {'Content-type': 'application/json',"Authorization":token}
            res = send_request(route="/check_answer/", js_obj = data, headers=headers)
            print(res)
            if "error" in res and type(res) == dict:
                self.bad_quiz(res["error"])
            elif "Error" in res:
                self.bad_quiz("Error server")
            if "ok" in res:
                self.id_que += 1
                if self.id_que < len(self.quests):
                    self.ids['id_answer'].text = ""
                    self.to_game()
                else:
                    self.id_que = 0
                    self.to_game_over()

    def to_game(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.get_screen("quiz0").ids.text_quest.text = self.quests[self.id_que]["quest"]
        # self.manager.get_screen("quiz").ids.id_quest.text = str(self.quests[0]["id_quest"])
        self.manager.current = 'quiz0'

    def to_game_over(self):
        token = read_token()
        if token:
            data = {"id_team":self.id_team, "count_que":len(self.quests)}
            headers = {'Content-type': 'application/json',"Authorization":token}
            res = send_request(route="/check_status_game/", js_obj = data, headers=headers)
            print(res)
            if "error" in res and type(res) == dict:
                self.bad_quiz(res["error"])
            elif "Error" in res:
                self.bad_quiz("Error server")
            elif "status" in res and res["status"]:
                text = "Результаты"                
            else:
                text = "Ожидаем других игроков"
                self.manager.get_screen("over").ids.reset.opacity = 1
                self.manager.get_screen("over").ids.reset.disabled = False
            self.manager.transition = SlideTransition(direction="right")
            self.manager.get_screen("over").ids.res.text = text
            self.manager.current = 'over'


class StartQuiz(Screen):
    all_ready = False
    i_ready = False
    id_team = ""

    def bad_start_quiz(self, message):
        layout = GridLayout(cols = 1, padding = 10)
        popupLabel = Label(text = message, size_hint = (0.2, 0.1),
            pos_hint = {"x" : 0.3, "top" : 0.8})
        closeButton = Button(text = "Назад", size_hint = (0.2, 0.1),
                              background_normal= '', background_color= '5ED05B')
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)       
        popup = Popup(title ='Ошибка!',
                      content = layout, size_hint =(None, None), size =(200, 200))  
        popup.open()   
        closeButton.bind(on_press = popup.dismiss)

    def disconnect(self):
        self.i_ready = False
        self.all_ready = False
        self.loading = ""
        self.not_ready("")
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'connected'

    # async def ready(self):
    #     pass

    def not_ready(self, __):
        token = read_token()
        self.id_team = self.manager.get_screen("start_quiz").ids.id_team.text
        if token:
            data = {"ready":False, "team":self.id_team}
            headers = {'Content-type': 'application/json',"Authorization":token}
            res = send_request(route="/set_ready/", js_obj = data, headers=headers)
            self.i_ready = False
            print(res)
            if "error" in res and type(res) == dict:
                self.bad_start_quiz(res["error"])
            elif "Error" in res:
                self.bad_start_quiz("Error server")
                
        if self.loading:
            self.loading.dismiss()

    def showLoading(self):
        layout = GridLayout(cols = 1, padding = 10)
        popupLabel = Label(text = "Собираем команду...", size_hint = (0.2, 0.1),
            pos_hint = {"x" : 0.3, "top" : 0.8})
        closeButton = Button(text = "Отмена", size_hint = (0.2, 0.1),
                              background_normal= '', background_color= '5ED05B')
        
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)
        self.loading = Popup(title ='Ожидаем...',
                      content = layout, size_hint =(None, None), size =(200, 200))  
        self.loading.open()
        closeButton.bind(on_press = self.not_ready)

    def check_all_ready(self):
        while not self.all_ready and self.i_ready:
            time.sleep(0.1)
            token = read_token()
            self.id_team = self.manager.get_screen("start_quiz").ids.id_team.text
            self.id_subject = self.manager.get_screen("start_quiz").ids.id_subject.text
            print(self.id_subject)
            if token:
                data = {"ready":True, "team":self.id_team, "subject":self.id_subject}
                headers = {'Content-type': 'application/json',"Authorization":token}
                res = send_request(route="/set_ready/", js_obj = data, headers=headers)
                print(res)
                if "error" in res and type(res) == dict:
                    self.bad_start_quiz(res["error"])
                elif "Error" in res:
                    self.bad_start_quiz("Error server")
                if "Ok" in res:
                    self.all_ready = True
                    self.quests = res["quests"]
                    print(res)
                    break
        self.loading.dismiss()
                # else:
                #     self.bad_start_quiz("Ждем подключения игроков!")

    def ready(self):
        self.showLoading() # showing pop up before starting thread
        # try:
        self.i_ready = True
        threading.Thread(target=lambda : self.check_all_ready()).start()
        print(self.all_ready)
        if self.all_ready:
            self.to_game()
        # except:
            # print("Error: unable to start thread")

    def to_game(self):
        if self.quests == []:
            token = read_token()
            self.id_team = self.manager.get_screen("start_quiz").ids.id_team.text
            self.id_subject = self.manager.get_screen("start_quiz").ids.id_subject.text
            if token:
                data = {"ready":True, "team":self.id_team, "subject":self.id_subject}
                headers = {'Content-type': 'application/json',"Authorization":token}
                res = send_request(route="/set_ready/", js_obj = data, headers=headers)
                print(res)
                if "error" in res and type(res) == dict:
                    self.bad_start_quiz(res["error"])
                elif "Error" in res:
                    self.bad_start_quiz("Error server")
                if "Ok" in res:
                    self.all_ready = True
                    self.quests = res["quests"]
        self.manager.transition = SlideTransition(direction="right")
        self.manager.get_screen("quiz0").ids.text_quest.text = self.quests[0]["quest"]
        # self.id_que = self.quests[0]["id_quest"]
        self.id_que = 0
        # self.manager.get_screen("quiz0").ids.id_quest.text = str(self.quests[0]["id_quest"])
        self.manager.current = 'quiz0'


