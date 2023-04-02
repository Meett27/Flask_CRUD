from todo_app import app
from flaskext.mysql import MySQL

db = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'meet@123'
app.config['MYSQL_DATABASE_DB'] = 'classes'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
db.init_app(app)