from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string' 

from todo_app import routes