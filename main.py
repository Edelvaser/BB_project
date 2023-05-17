from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import os
from kivy.uix.widget import Widget
from connected import Connected
from quiz import Quiz_0, Quiz_1, StartQuiz
from over import Over
from dop_function import check_email, check_password, write_token, read_token, send_request #, popFun
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.network.urlrequest import UrlRequest
import json

  
class Login(Screen):
    def do_login(self, loginText, passwordText):
        app = App.get_running_app()

        app.username = loginText
        app.password = passwordText
        message = ""
        if not check_email(loginText): message = "Неверный адрес"
        if message:
            self.message = message
            self.bad_auth(message)
        else:
            self.manager.transition = SlideTransition(direction="left")
            data = {"login":app.username, "password":app.password}
            headers = {'Content-type': 'application/json'}
            res = send_request(route="/auth/", js_obj = data, headers=headers)
            if "token" in res:
                print(type(res))
                write_token(res)
                self.manager.current = 'connected'
                self.manager.transition = SlideTransition(direction="left")
            elif "error" in res and type(res) == dict:
                self.bad_auth(res["error"])
            elif "error" in res:
                self.bad_auth("Error server")
            else:
                self.bad_auth("Ошибка!")

        app.config.read(app.get_application_config())
        app.config.write()

    def goto_reg(self):
        app = App.get_running_app()

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'reg'

        app.config.read(app.get_application_config())
        app.config.write()

    def resetForm(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""

    def bad_auth(self, message):
        print(message)
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

class Register(Screen):
    def bad_reg(self, message):
        print(message)
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


    def do_reg(self, loginText, passwordText, repPassText):
        app = App.get_running_app()

        app.username = loginText
        app.password = passwordText
        app.rep_pass = repPassText
        message = ""
        if not check_email(loginText): message = "Неверный адрес"
        elif not check_password(passwordText): message = "Неподходящий пароль"
        elif passwordText != repPassText: message = "Пароли не совпадают"
        if message:
            self.message = message
            self.bad_reg(message)
        else:
            self.manager.transition = SlideTransition(direction="left")
            data = {"login":app.username, "password":app.password, "rep_pass":app.rep_pass}
            headers = {'Content-type': 'application/json'}
            res = send_request(route="/reg/", js_obj = data, headers=headers)
            print(type(res))
            if "token" in res:
                write_token(res)
                self.manager.current = 'connected'
            elif "error" in res and type(res) == dict:
                self.bad_reg(res["error"])
            elif "error" in res:
                self.bad_reg("Error server")
            else:
                print(res)
                self.bad_reg("Ошибка!")

        app.config.read(app.get_application_config())
        app.config.write()

    def goto_login(self):
        app = App.get_running_app()
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'login'

        app.config.read(app.get_application_config())
        app.config.write()

    def resetForm(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""

class MainApp(App):
    username = StringProperty(None)
    password = StringProperty(None)

    def build(self):
        manager = ScreenManager()
        self.rddm = ""
        self.id_team = 0

        if os.path.exists("infoData"):
            token = read_token()
            headers = {'Content-type': 'application/json', "Authorization":token}
            res = send_request(route="/auth/", js_obj = {"1":1}, headers=headers)
            if res is None or "token" not in res:
                manager.add_widget(Login(name='login'))
                manager.add_widget(Register(name='reg'))
                manager.add_widget(Connected(name='connected'))
            else:
                manager.add_widget(Connected(name='connected'))
                manager.add_widget(Login(name='login'))
                manager.add_widget(Register(name='reg'))
        else:
            manager.add_widget(Login(name='login'))
            manager.add_widget(Register(name='reg'))
            manager.add_widget(Connected(name='connected'))
        manager.add_widget(StartQuiz(name='start_quiz'))
        manager.add_widget(Quiz_0(name='quiz0'))
        manager.add_widget(Quiz_1(name='quiz1'))
        manager.add_widget(Over(name='over'))
        return manager

    def get_application_config(self):
        if(not self.username):
            return super(MainApp, self).get_application_config()

        conf_directory = self.user_data_dir + '/' + self.username

        if(not os.path.exists(conf_directory)):
            os.makedirs(conf_directory)

        return super(MainApp, self).get_application_config(
            '%s/config.cfg' % (conf_directory)
        )

if __name__ == '__main__':
    MainApp().run()