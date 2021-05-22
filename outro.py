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

    def conexao_bd(self, user, password, tipo, medida, quantidade, value):
        global conn, cursor
        self.user = user
        self.password = password
        status = True
        try:
            conn = pyodbc.connect('Driver={SQL Server};'
                                  f'Server={os.environ["Server"]};'
                                  f'Database={os.environ["Database"]};'
                                  'Trusted_Connection=no;'
                                  f'UID={user.text};'
                                  f'PWD={password.text};')
            cursor = conn.cursor()
        except pyodbc.InterfaceError:
            print("O nome de Usuário ou a Palavra Passe digitada é incorreta! \n\t\tTente Novamente")
            user.text = ''
            password.text = ''
            status = False
            return status
        if user.text == '' or password.text == '':
            status = False
            print("O nome de Usuário ou a Palavra Passe digitada é incorreta! \n\t\tTente Novamente")
            return status
        if value == 1:
            conn.commit()
            cursor.close()
            conn.close()
            status = True
            return status
        elif value == 2:
            #print(f"{type(tipo)}: {tipo}\n{type(medida)}: {medida}\n{type(quantidade)}: {quantidade}\n{type(user.text)}: {user.text}")
            cursor.execute(f"""INSERT INTO {os.environ['Database']}.dbo.ENTRADAS (TIPO, MEDIDA, QUANTIDADE, NOME) VALUES ('{tipo}', '{medida}', {int(quantidade)}, '{user.text}')""")
            conn.commit()
            cursor.close()
            conn.close()
            return "Linha de Entrada Adicionada"
        else:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {os.environ['Database']}.dbo.SAIDAS ({tipo}, {medida}, {quantidade}) " "values(?,?,?)",
                row.value, row.medida, row.quantidade)
            conn.commit()
            cursor.close()
            conn.close()
            return "Linha de Saida Adicionada"

    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()