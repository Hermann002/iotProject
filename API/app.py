from flask import Flask, request
from database.dbaction import insertDB
import datetime

app = Flask(__name__)

@app.route('/api/add_message/', methods=['GET', 'POST'])
def add_message():
    content = request.json
    content['created'] = datetime.datetime.now()
    print(content)
    insertDB(content)
    return "ok"

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)