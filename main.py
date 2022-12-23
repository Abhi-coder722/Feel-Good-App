from datetime import datetime
from fileinput import filename
from kivy.app import App
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json
import glob
from pathlib import Path
import random

Builder.load_file('design.kv')
 
class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current='sign_up_screen'
    def login(self,uname,pword):
        if uname != None and pword != None:
            with open('users.json') as file:
                users=json.load(file)
            if uname in users and users[uname]['password'] == pword:
                self.manager.current='login_screen_success'
            else:
                anim=Animation(color=(0.6,0.7,0.1,1))
                anim.start(self.ids.login_wrong)
                self.ids.login_wrong.text='Wrong id or password !'
        else:
            self.ids.login_wrong.text='Please enter the id and password!'

    def forgot(self):
        self.manager.current='forgot_screen'


class ForgotScreen(Screen):
    def get_pass(self,uname,sec):
        if uname and sec != None:
            with open('users.json','r') as file:
                users=json.load(file)
            if uname in users and users[uname]['security_question'] == sec:
                self.ids.give_pass.text=(users[uname]['password'])
            else:
                self.ids.give_pass.text=('Wrong username or security')
        else:
            self.ids.give_pass.text=('Enter both the sections !')
    def go_to_login(self):
        self.manager.current="login_screen"
class ImageButton(ButtonBehavior,HoverBehavior,Image):
    pass
 
class RootWidget(ScreenManager):
    pass
 
class SignUpScreen(Screen):
    def add_user(self,uname,pword,sec):
        if uname and pword and sec !=None:
            with open('users.json') as file:
                users=json.load(file)
            users[uname]={'username':uname,'password':pword,'security_question':sec,'created':datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
            with open("users.json",'w') as file:
                json.dump(users,file)
            self.manager.current='sign_up_screen_success'
            self.ids.sign_success.text=('Sign in success!')
        else:
            self.ids.sign_success.text=('Enter all the sections ..')

class SignUpScreenSuccess(Screen):
    def go_to_login(self):

        self.manager.transition.direction='right'
        self.manager.current='login_screen'


class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction='right'
        self.manager.current='login_screen'
    def get_quote(self,feel):
        feel=feel.lower()
        available_feelings=['happy','sad','unloved','single']

        if feel in available_feelings:
            with open(f'{feel}.txt',encoding="utf8") as file:
                quotes=file.readlines()
            self.ids.quote.text=random.choice(quotes)
        else:
            self.ids.quote.text=("Try another feeling..")
        



class MainApp(App):
    def build(self):
        return RootWidget()


 
if __name__ == "__main__":
    MainApp().run() 