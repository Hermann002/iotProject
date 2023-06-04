from .db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

class User:

    def __init__(self, username, useremail, password):
        self.username = username
        self.useremail = useremail
        self.password = password
        self.token = str(uuid.uuid1())
        self.__is_admin = False

    def insertUser(self):
        db = get_db()
        db.execute(
                    "INSERT INTO user (username, useremail, password, token) VALUES (?, ?, ?, ?)",
                    (self.username, self.useremail, generate_password_hash(self.password), self.token),
                )
        db.commit()

    def get_is_admin(self):
        return self.__is_admin
    
    def set_is_admin(self, is_admin):
        self.__is_admin = is_admin