from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import NumericProperty
from dop_function import send_request, read_token
import os

class Connected(Screen):
    rddm = ""
    id_team = ""
    def bad_connect(self, message):
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
        os.remove("infoData")
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()
    
    def spinner_clicked(self, value):
        app = App.get_running_app()
        self.rddm = value
        print(self.rddm)
        app.config.read(app.get_application_config())
        app.config.write()
    
    def to_team(self, id_team):
            app = App.get_running_app()
        # try:
            if not id_team.isdigit():
                self.bad_connect("Неверный номер команды!")
            else:
                self.id_team = int(id_team)
                token = read_token()
                if token:
                    data = {"id_team": self.id_team, "token": token}
                    headers = {'Content-type': 'application/json',"Authorization":token}
                    res = send_request(route="/check_team/", js_obj = data, headers=headers)
                    print(res)
                    if "error" in res and type(res) == dict:
                        self.bad_connect(res["error"])
                    elif "Error" in res:
                        self.bad_connect("Error sever")
                    else:
                        self.manager.get_screen("start_quiz").ids.id_team.text = str(self.id_team)
                        self.manager.transition = SlideTransition(direction="right")
                        self.manager.current = 'start_quiz'
        # except:
        #     self.bad_connect("Ошибка, попробуйте еще раз!")

            app.config.read(app.get_application_config())
            app.config.write()
        
    def create_team(self):
        app = App.get_running_app()
        self.id_team = NumericProperty(0)
        try:
            if not self.rddm:
                self.bad_connect("Выберите направление!")
            else:
                token = read_token()
                if token:
                    self.rddm = "СЛУЖИ ОТЕЧЕСТВУ!"
                    data = {"name":self.rddm}
                    headers = {'Content-type': 'application/json',"Authorization":token}
                    res = send_request(route="/create_team/", js_obj = data, headers=headers)
                    print(res)
                    if "error" in res and type(res) == dict:
                        self.bad_connect(res["error"])
                    elif "Error" in res:
                        self.bad_connect("Error sever")
                    else:
                        self.id_team = res["id_team"]
                        app.id_team = res["id_team"]
                        app.rddm = self.rddm
                        self.manager.transition = SlideTransition(direction="right")
                        self.manager.get_screen("start_quiz").ids.id_team.text = str(res["id_team"])
                        self.manager.get_screen("start_quiz").ids.id_subject.text = self.rddm
                        self.manager.current = 'start_quiz'
        except:
            self.bad_connect("Ошибка, попробуйте еще раз!")
        app.config.read(app.get_application_config())
        app.config.write()

