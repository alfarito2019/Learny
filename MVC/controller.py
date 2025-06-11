# controller.py
from model import UserModel
from view import LoginView
import tkinter as tk

class AppController:
    def __init__(self, root):
        self.model = UserModel()
        self.view = LoginView(root)
        self.view.set_login_action(self.login)

    def login(self):
        documento, clave = self.view.get_credentials()
        if self.model.validate_user(documento, clave):
            user_data = self.model.get_user_data(documento)
            self.view.show_message(f"Bienvenido, {user_data['Nombre']}")
            # Aquí puedes navegar a otra vista
        else:
            self.view.show_message("Credenciales incorrectas.")
