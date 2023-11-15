import configparser
import os
class Settings():
    def __init__(self):
        self.is_exist=True
        if os.path.isfile('settings.ini'):
            self.c=configparser.ConfigParser()
            self.c.read('settings.ini')
        else:
            self.is_exist=False
    def set_mssql(self, name_server, name_user, password):
        with open("settings.ini", "w", encoding='utf-8') as f:
            f.write("[MSSQL]\n")           
            f.write(f"NAME_SERVER={name_server}\n")
            f.write(f"NAME_USER={name_user}\n")
            f.write(f"PASSWORD={password}\n")
    def get_mssql(self):
        if self.is_exist:
            return self.c["MSSQL"]["NAME_SERVER"],self.c["MSSQL"]["NAME_USER"],self.c["MSSQL"]["PASSWORD"]
        return False
    def set_mail(self, login_mail, password):
        with open("settings.ini", "a", encoding='utf-8') as f:
            f.write("[MAIL]\n")           
            f.write(f"LOGIN_MAIL={login_mail}\n")
            f.write(f"PASSWORD={password}\n")
    def get_mail(self):
        if self.is_exist:
            return self.c["MAIL"]["LOGIN_MAIL"],self.c["MAIL"]["PASSWORD"]
