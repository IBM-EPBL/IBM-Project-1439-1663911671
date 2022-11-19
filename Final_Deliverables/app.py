from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail,Message
import ibm_db
import re

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'tmkssolution1234@gmail.com'
app.config['MAIL_PASSWORD'] = 'xyfxjnripeytrqhk'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail=Mail(app)
  
app.secret_key = 'a'
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32716;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=jzc43091;PWD=PI8VtGRvZlSVT65A",'','')


@app.route('/')

def homer():
    return render_template('home.html')

@app.route('/agent')
def agent():
    return render_template("agent.html")

@app.route('/admin')
def agnt():
    return render_template("admin.html")
@app.route('/free')
def free():
    return render_template("free.html")


@app.route('/ForgotPassword', methods=['GET','POST'])
def ForgotPassword():
     if request.method=="POST":
        name=request.form['name']
        email=request.form['email']
        message=Message(subject, sender='tmkssolution1234@gmail.com', recipients=['johncaesar07@gmail.com', 'murasutamil2002@gmail.com','kamaleshwaran1123@gmail.com','hellsprince26@gmail.com'])

        message.body="""
        

        Hey Guys we have work.

        The Client sends a Query,

        Name - {}

        Email - {}
        
        Thank you
        
        """.format(name,email)
  
        mail.send(message)

        return render_template("success.html")
     return render_template("ForgotPassword.html")


@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid=  account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in successfully !'
            
            msg = 'Logged in successfully !'
            return render_template('customer.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

        

   
@app.route('/register', methods =['GET', 'POST'])
def registet():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            insert_sql = "INSERT INTO  users VALUES (?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/customer')
def dash():
   

    
    return render_template('customer.html')

@app.route('/plan')
def plan():
    return render_template('plan.html')

@app.route('/adminlogin')
def alogin():
    return render_template('adminlogin.html')






@app.route('/logout')

def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('home.html')





@app.route("/form", methods=['GET', 'POST'])
def form():
    if request.method=="POST":
        name=request.form['name']
        email=request.form['email']
        suppoter=request.form['suppoter']
        subject=request.form['subject']
        query=request.form['query']
        message=Message(subject, sender='tmkssolution1234@gmail.com', recipients=['johncaesar07@gmail.com', 'murasutamil2002@gmail.com','kamaleshwaran1123@gmail.com','hellsprince26@gmail.com'])

        message.body="""
        

        Hey Guys we have work.

        The Client sends a Query,

        Name - {}

        Email - {}

        Support - {}

        Query :  {}
            
        
        Thank you
        
        """.format(name,email,suppoter,query)
  
        mail.send(message)

        return render_template("success.html")
    return render_template("form.html")


if __name__ == '__main__':
   app.run(host='0.0.0.0')
