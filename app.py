from src.utils.connection_cassandra import cassandra_user
from flask import Flask, render_template, request
import re

app = Flask(__name__)
cassandra = cassandra_user()


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def reg():
    return render_template('registration.html')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')
    user = cassandra.get_useraccount(f"SELECT * FROM user WHERE email = '{email}' AND Password = '{password}' ALLOW FILTERING ")
    print("----------", user)
    if len(user) > 0:
        return render_template('success.html')
    else:
        return render_template('home.html', msg = "Wrong Userid and Password")


@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')

    
    
    user_account = cassandra.get_useraccount(f"SELECT * FROM user WHERE email = '{email}' ALLOW FILTERING ")
    if len(user_account) > 0:
        msg = 'EmailId already exists !'
        return render_template('registration.html', msg = msg)
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        msg = 'Invalid email address !'
        return render_template('registration.html', msg = msg)
    elif not re.match(r'[A-Za-z0-9]+', name):
        msg = 'Username must contain only characters and numbers !'
        return render_template('registration.html', msg = msg)
    elif not name or not password or not email:
        msg = 'Please fill out the form !'
        return render_template('registration.html', msg = msg)
    else:
        verify_count = cassandra.adduser(f"INSERT INTO user (email , name , password) VALUES ('{email}', '{name}',  '{password}')")
        return render_template('success.html')


if __name__ == "__main__":
    app.run(debug=True)