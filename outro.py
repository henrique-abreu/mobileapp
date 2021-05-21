from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image, Widget
from kivy.properties import ObjectProperty
import pyodbc
import os

class EntradaWindow(Screen):
    def on_spinner_select(self, text):
        self.text = text
        pass

class SaidaWindow(Screen):
    def on_spinner_select(self, text):
        self.text = text
        pass

class MenuWindow(Screen):
    pass

class LoginWindow(Screen, Widget):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("layout.kv")

class MyMainApp(App):

    user = ObjectProperty(None)
    password = ObjectProperty(None)

    def insert_row(self, *args):
        '''
        conn = pyodbc.connect('Driver={SQL Server};'
                              f'Server={os.environ["Server"]};'
                              f'Database={os.environ["Database"]};'
                              'Trusted_Connection=no;'
                              f'UID={user.text};'
                              f'PWD={password.text};')

        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {os.environ['Database']}.dbo.ENTRADAS ({value}, {medida}, {quantidade}) " "values(?,?,?)",
                       row.value, row.medida, row.quantidade)
        conn.commit()
        cursor.close()
        conn.close()
    '''
        print(*args)
    def check_login(self, user, password):
        self.user = user
        self.password = password
        status = True
        '''
        try:
            conn = pyodbc.connect('Driver={SQL Server};'
                                  f'Server={os.environ["Server"]};'
                                  f'Database={os.environ["Database"]};'
                                  'Trusted_Connection=no;'
                                  f'UID={user.text};'
                                  f'PWD={password.text};')

            cursor = conn.cursor()
            conn.commit()
            cursor.close()
            conn.close()
        except pyodbc.InterfaceError:
            print("O nome de Usuário ou a Palavra Passe digitada é incorreta! \n\t\tTente Novamente")
            status = False'''

        if user.text == '' or password.text == '':
            status = False
            print("O nome de Usuário ou a Palavra Passe digitada é incorreta! \n\t\tTente Novamente")
        return user.text, password.text, status

    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()