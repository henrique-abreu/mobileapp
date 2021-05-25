from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image, Widget
from kivy.properties import ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import pyodbc
import os

class Alert(Popup):

    def __init__(self, title, text):
        super(Alert, self).__init__()
        content = AnchorLayout(anchor_x='center', anchor_y='bottom')
        content.add_widget(
            Label(text=text, halign='left', valign='top')
        )
        ok_button = Button(text='Ok', size_hint=(None, None), size=(Window.width / 8, Window.height / 8))
        content.add_widget(ok_button)

        popup = Popup(
            title=title,
            content=content,
            size_hint=(None, None),
            size=(Window.width / 1.5, Window.height / 1.5),
            auto_dismiss=True,
        )
        ok_button.bind(on_press=popup.dismiss)
        popup.open()

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

    def corrigir_nome(self, user):
        self.user = user
        nome = user.split(" ")
        correcao = ""
        for i in nome:
            correcao += str(i).capitalize() + " "
        return correcao.strip()

    def conexao_bd(self, user, password, tipo, medida, quantidade, value):
        global conn, cursor
        self.user = user
        self.password = password
        self.tipo = tipo
        self.medida = medida
        self.quantidade = quantidade
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
            Alert(title='Erro no Login', text='O nome de Usuário ou a Palavra Passe digitada é incorreta! \nTente Novamente!') #popup source: https://stackoverflow.com/questions/42374377/error-with-kivy-login-screen-and-popup
            user.text = ''
            password.text = ''
            status = False
            return status
        if user.text == '' or password.text == '':
            status = False
            Alert(title='Erro no Login', text='O nome de Usuário ou a Palavra Passe digitada é incorreta! \nTente Novamente')
            return status
        if value == 1:
            conn.commit()
            cursor.close()
            conn.close()
            status = True
            return status
        elif value == 2:
            cursor.execute(f"""INSERT INTO {os.environ['Database']}.dbo.ENTRADAS (TIPO, MEDIDA, QUANTIDADE, NOME) VALUES ('{tipo}', '{medida}', {int(quantidade)}, '{self.corrigir_nome(user.text)}')""")
            conn.commit()
            cursor.close()
            conn.close()
            Alert(title='Sucesso', text='Linha de Entrada Adicionada')
            pass
        elif value == 3:
            cursor = conn.cursor()
            cursor.execute(
                f"""INSERT INTO {os.environ['Database']}.dbo.SAIDAS (TIPO, MEDIDA, QUANTIDADE, NOME) VALUES ('{tipo}', '{medida}', {int(quantidade)}, '{user.text}')""")
            conn.commit()
            cursor.close()
            conn.close()
            Alert(title='Sucesso', text='Linha de Saída Adicionada')
            pass

    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()