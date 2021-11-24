from src.utils.connection_cassandra import cassandra_user
from flask import Flask, redirect, url_for, render_template, request , session
import re
from werkzeug.utils import secure_filename
import os
import time




app = Flask(__name__)
app.secret_key = 'DB128%^#*(%$C345'
cassandra = cassandra_user()

@app.context_processor
def context_processor():
    loggedin=False
    if 'loggedin' in session:
        loggedin=True
        
    return dict(loggedin=loggedin)

@app.route('/login')
def login():
    if 'loggedin' in session:
        return render_template('success.html')
    else:
        if request.method == "GET":
            return render_template('login.html')
    


@app.route('/register')
def reg():
    return render_template('registration.html')


@app.route('/')
def home():
    return render_template('home.html')

# @app.route('/index', methods=['GET', 'POST'])
# def index():
#     try:
#         if 'loggedin' in session:
#             return render_template('index.html')
#         else:
#             return redirect(url_for('login'))
#     except Exception as e:
#         print("8888888888888888888888888888888888",e)


# @app.route('/project', methods=['GET', 'POST'])
# def project():
#     try: 
#         if 'loggedin' in session:
#             if request.method == "GET":
#                 return render_template('project.html',loggedin=True)
#             else:
#                 name = request.form['name']
#                 description = request.form['description']
#                 f = request.files['file']

#                 ALLOWED_EXTENSIONS = ['csv', 'tsv', 'json', 'xml']
#                 msg = ''
#                 if not name.strip():
#                     msg = 'Please enter project name'
#                 elif not description.strip():
#                     msg = 'Please enter project description'
#                 elif f.filename.strip() == '':
#                     msg = 'Please select a file to upload'
#                 elif f.filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
#                     msg = 'This file format is not allowed, please select mentioned one'

#                 if msg:
#                     return render_template('new_project.html', msg=msg)

#                 filename = secure_filename(f.filename)
#                 f.save(os.path.join("data", filename))
#                 timestamp =round(time.time() * 1000)
#                 table_name = f"{name}_{timestamp}"
#                 file = f"data/{filename}"

#                 if filename.endswith('csv'):
#                    status= cassandra.push_csv_to_database(file,table_name)
#                    print(cassandra.retrive_dataset(table_name))

#                 elif filename.endswith('tsv'):
#                     status = cassandra.push_tsv_to_database(file, table_name)
#                     print(cassandra.retrive_dataset(table_name))

#                 if status==1:
#                    userId = session.get('id')
#                    status = 1
#                    query=f"""INSERT INTO tblProjects (UserId, Name, Description, Status, 
#                    Cassandra_Table_Name) VALUES
#                    ("{userId}", "{name}", "{description}", "{status}", "{table_name}")"""

#                    rowcount = mysql.insert_record(query)

#                    if rowcount > 0:
#                        return redirect(url_for('index'))
#                    else:
#                        msg="Error while creating new Project"

#                 return render_template('project.html',msg=msg)
#         else:
#             return redirect(url_for('login'))
    
#     except Exception as e:
#         print(e)




@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')
    user = cassandra.get_useraccount(f"SELECT * FROM user WHERE email = '{email}' AND Password = '{password}' ALLOW FILTERING ")
    print("----------", user)
    if len(user) > 0:
         session['loggedin'] = True
         
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