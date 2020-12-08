
from kivy import Config
from kivy.clock import Clock
from kivymd.app import MDApp
from models.MapScreen import MapScreen
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from data import db
import os

class Login(Screen):
    def do_login(self, loginText, passwordText):
        if db.authentication(loginText, passwordText):
            print("authentication...")
            self.manager.current = 'homepage'
        else:
            self.ids['wrong_data'].text = "Wrong password or login"


class Homepage(Screen):
    def __init__(self,**kvargs):
        super(Homepage, self).__init__(**kvargs)
        from models.location import location
        latitude,longitude,self.ids['current_location'].text =location.get_current_location()
        from models.map import Map
        self.map=Map(zoom=8, lat=latitude,lon=longitude)
        x,y=self.map.get_window_xy_from(latitude,longitude,16)
        self.map.set_zoom_at(9,x,y)


    def show_location(self):
       pass


class TouristApp(MDApp):

    def __init__(self,**kvargs):
        super(TouristApp, self).__init__(**kvargs)
        self.manager=None

    def build(self):

        self.load_all_kv_files("kivy_file")
        self.manager = ScreenManager()
        self.manager.add_widget(Login(name='login'))
        from models.sign_up import Signup
        self.manager.add_widget(Signup(name='signup'))
        self.manager.add_widget(Homepage(name='homepage'))
        self.manager.add_widget(MapScreen(name="mapScreen"))
        Window.size = (480, 640)

        return self.manager

    def load_all_kv_files(self, directory_kv_files):

         for kv_file in os.listdir(directory_kv_files):

             kv_file = os.path.join(directory_kv_files, kv_file)

             if os.path.isfile(kv_file):

                Builder.load_file(kv_file)


    def get_screen_manager(self):
       return self.manager
if __name__ == '__main__':
    Clock.max_iteration = 100
    TouristApp().run()
