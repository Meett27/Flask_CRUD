import re
from todo_app import app
from todo_app.db_config import db
from flask import request, render_template, flash, redirect, url_for, session,json


@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
     # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('index.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/login',methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        u_name = request.form.get('u_name')
        password = request.form.get('password')
        data = (u_name, password)
        sql = """SELECT * FROM users WHERE email=%s and password=%s""" 
        conn = db.connect()
        csr = conn.cursor()
        csr.execute(sql,data)
        u_act = csr.fetchone()

        if u_act:
            user = list(u_act)
             # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = user[0]
            session['username'] = user[1] +" "+ user[2]
            session['admin'] = user[5]
            # Redirect to home page
            flash('Logged in successfully!')
            return redirect('/home')
        else:
            flash('Invalid username / password')
    return render_template("login.html")

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('isAdmin', None)
    # Redirect to login page
    return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':
        first_name = request.form.get('f_name')
        last_name = request.form.get('l_name')
        email = request.form.get('email')
        password = request.form.get('password')
        data = (first_name, last_name, email,password)

        sql = """SELECT * FROM users WHERE email=%s""" 
        conn = db.connect()
        csr = conn.cursor()
        csr.execute(sql,email)
        u_act = csr.fetchone()
        
        if u_act:
            flash("user already exist!!")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("invalid email address!!")
        else:
            sql = """INSERT INTO users(first_name, last_name, email, password) VALUES(%s,%s,%s,%s)"""
            csr.execute(sql, data)
            conn.commit()
            csr.close()
            conn.close()
            flash("User register successfully")
            return redirect('/login')
    return render_template("register.html")


@app.route('/courses')
def courses():
    data_dict = {}
     # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        sql = "SELECT * FROM courses"
        conn = db.connect()
        csr = conn.cursor()
        csr.execute(sql)
        result = csr.fetchall()
        
        

        return render_template("courses.html",data=result)
        # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    


@app.route('/add_course', methods=['POST', 'GET'])
def add_courses():

    if request.method == 'POST':
        course_id = request.form.get('c_id')
        title = request.form.get('c_title')
        desc = request.form.get('c_desc')
        data = (course_id,title,desc)
        sql = "INSERT INTO courses(id, title, description) VALUES (%s,%s,%s)"
        conn = db.connect()
        csr = conn.cursor()
        csr.execute(sql, data)
        conn.commit()
        csr.close()
        conn.close()
        flash("data added succesfully.")
        return redirect(url_for('courses'))
    return render_template("add_course.html")


@app.route('/update_course/<int:id>', methods=['GET'])
def get_course(id):
    if request.method == 'GET':
        conn = db.connect()
        csr = conn.cursor()
        sql="SELECT * FROM courses WHERE id=%s"
        csr.execute(sql,id)
        course = csr.fetchall()
        csr.close()
        conn.close()
        return render_template('update_course.html', data=list(course))

@app.route('/update_course', methods=['POST'])
def update_course():
    if request.method == 'POST':
        conn = db.connect()
        csr = conn.cursor()
        id = request.form.get('c_id')
        title = request.form.get('c_title')
        desc = request.form.get('c_desc')
        data = (title,desc,id)
        print(data)
        sql = """UPDATE courses SET title=%s, description=%s WHERE id=%s"""
        csr.execute(sql,data)
        conn.commit()
        csr.close()
        conn.close()
        flash("data updated succesfully.")
        return redirect(url_for('courses'))

@app.route('/add_enrollment', methods=['POST','GET'])
def enrollment():
    if request.method == 'POST':
        c_id = request.form.get('c_id')
        data = ()
        sql = """INSERT INTO enrollment (user_id, course_id) VALUES({0},{1})""".format(session['id'], c_id)
        conn = db.connect()
        csr = conn.cursor()
        csr.execute(sql)
        csr.close()
        conn.close()
        flash("course enrolled succesfully.")
        return redirect(url_for('courses'))

@app.route('/enrollments', methods=['POST', 'GET'])
def get_enrollment():
    sql = """SELECT * FROM enrollment where """
    conn = db.connect()
    csr = conn.cursor()
    result = csr.execute(sql)
    csr.close()
    conn.close()
    return render_template('enrollment.html')
