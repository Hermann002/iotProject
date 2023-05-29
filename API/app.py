from flask import Flask, request, render_template
from models.dbaction import insertDB, findUser
import datetime
from models.models import User
import uuid
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

@app.route('/api/')
def home():
    return render_template("blog/home.html")

@app.route('/api/add_message/', methods=['GET', 'POST'])
def add_message():
    content = request.json

    #add field that content the date when data fetch
    content['created'] = datetime.datetime.now()
    print(content)

    # insert in the mongo database
    try:
        insertDB(content)
    except Exception as e:
        print("erreur d'envoie")

    return "ok"

@app.route('/api/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        content = request.form
        print(type(content))
        userName = content['userName']
        userSurname = content['userSurname']
        userEmail = content['userEmail']
        password = content['password']
        userNumber = content['number']

        user = User(userName, userSurname, userNumber, userEmail, generate_password_hash(password))
        token = str(uuid.uuid1()) 
        
        #check if user already exist
        if findUser(userEmail, userNumber):
            return f"l'utilisateur {userName} existe déja !"
        else:
            # insert in mongo database
            try:
                user.signUp(token)
            except Exception as e:
                print(e) 
            return render_template("auth/token.html", key = token)
    
    else:
        return render_template('auth/register.html')

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)