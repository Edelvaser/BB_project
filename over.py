from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from dop_function import send_request, read_token
from kivy.uix.boxlayout import BoxLayout
from kivy.base import EventLoop
from math import ceil
from dop_function import txt_end_word

class Over(Screen):
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
        self.manager.get_screen('start_quiz').quests = []
        self.manager.current = 'connected'
    
    def reset_result(self):
        token = read_token()
        self.id_team = self.manager.get_screen("start_quiz").id_team
        self.id_subject = self.manager.get_screen("start_quiz").id_subject
        # self.quests = self.manager.get_screen('start_quiz').quests[:]
        # try:
        #     self.id_que =  self.manager.get_screen("quiz1").id_que
        # except:
        #     self.id_que = self.manager.get_screen("start_quiz").id_que
        if token:
            data = {"id_team":self.id_team}
            headers = {'Content-type': 'application/json',"Authorization":token}
            res = send_request(route="/reset_result/", js_obj = data, headers=headers)
            count_quiz = len(self.manager.get_screen('start_quiz').quests)
            print(res)
            if "error" in res and type(res) == dict:
                self.bad_quiz(res["error"])
            elif "error" in res:
                self.bad_quiz("Error server")
            if "ok" in res:
                print(res)
                if res["ok"] >= 0:
                    perc = ceil(res["ok"]/count_quiz*100)
                    if perc >= 90:
                        self.text = "Отлично! "
                    elif perc >= 75:
                        self.text = "Хорошо! "
                    elif perc >= 50:
                        self.text = "Нормально! "
                    else:
                        self.text = "Вам надо побольше \nузнать об этой теме.\n"
                    self.result = res["ok"]
                    txt_ocon = txt_end_word(res["ok"])
                    self.manager.get_screen("over").ids.res.text = self.text + \
                                            "Вы набрали {0} {1}!".format(res["ok"], txt_ocon)

    def to_game(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.get_screen("quiz1").ids.text_quest.text = self.quests[self.id_que]["quest"]
        # self.manager.get_screen("quiz").ids.id_quest.text = str(self.quests[0]["id_quest"])
        self.manager.current = 'quiz1'

    def to_result(self, res):
        self.manager.transition = SlideTransition(direction="right")
        # self.manager.get_screen("results").ids.text_quest.text = self.result
        # self.manager.get_screen("quiz").ids.id_quest.text = str(self.quests[0]["id_quest"])
        self.manager.current = 'results'