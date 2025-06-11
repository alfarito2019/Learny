# model.py
import pandas as pd

class UserModel:
    def __init__(self, excel_path='BD.xlsx'):
        self.excel_path = excel_path
        self.df = pd.read_excel(excel_path)

    def validate_user(self, documento, clave):
        user = self.df[(self.df['Cedula'] == documento) & (self.df['Clave'] == clave)]
        return not user.empty

    def get_user_data(self, documento):
        return self.df[self.df['cedula'] == documento].to_dict('records')[0]
