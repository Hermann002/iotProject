from database import connect, insertUser
from flask import request

class User:
    is_admin = False

    def __init__(self, userName, userSurname, userNumber, userEmail, password):
        self.userName = userName
        self.userEmail = userEmail
        self.userSurname = userSurname
        self.userNumber = userNumber
        self.password = password

    def signUp(self, token):
        insertUser({
            'nom' : self.userName,
            'prenom': self.userSurname,
            'numero': self.userNumber,
            'email': self.userEmail,
            'password': self.password,
            'token': token
        })