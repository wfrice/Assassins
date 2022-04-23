from flask import Flask, flash, redirect, render_template, request, session, abort
from passlib.hash import sha256_crypt
import mysql.connector as mariadb
import cgi, os
import cgitb
from psutil import users; cgitb.enable()
from werkzeug.utils import secure_filename
import pythonlogin.newBase as newBase




app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = 'static/uploads'
app.config['MAX_CONTENT-PATH'] = 16 * 1080 * 1080




ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def write_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def home():
  try:
    mariadb_connect = mariadb.connect(user='root', password='rootpassword', database='Assassins', host='assassins-db', port="3306")
  except:
    print('error')
    return render_template('settings.html')

  if not session.get('logged_in'):
    print(app.static_folder)
    return render_template('login.html')
  else:
    cur = mariadb_connect.cursor(buffered=True)
    
    cur.execute(f'select uid from first where email="{session.get("email")}"')
    uid = cur.fetchall()[0][0]
    
    cur.execute('select * from first')
    users = cur.fetchall()
    
    for i in range(len(users)):
      if users[i][2] != session.get('email'):
        continue
      else:
        user = users[i-1]
        write_file(users[i-1][4], os.path.join(app.config['UPLOAD_FOLDER'], 'prof.png'))

    
    mariadb_connect.commit()
    cur.close()

    return render_template('index.html', user = user[1])

@app.route('/startSettings', methods=['POST'])
def startSettings():
    result = False
    if "connect" in request.form:
      newBase.initDatabase()
    return redirect('/')


@app.route('/login', methods=['POST'])
def do_admin_login():
  login = request.form

  email = login['email']
  password = login['password']

  mariadb_connect = mariadb.connect(user='root', password='rootpassword', database='Assassins', host='assassins-db', port="3306")
  cur = mariadb_connect.cursor(buffered=True)
  data = cur.execute(f'SELECT * FROM first WHERE email="{email}";')
  try:
    data = cur.fetchone()[3]
    mariadb_connect.commit()
    cur.close()

    if sha256_crypt.verify(password, data):
      account = True
    else:
      account = False

    if account:
      session['logged_in'] = True
      session['email'] = email
    else:
      flash('wrong password!')
    print('error')
    return redirect('/')
  except:
    return redirect('/')

@app.route('/register')
def register():
  return render_template('register.html')

@app.route('/registerAccount', methods=['POST', 'GET'])
def registerAccount():
  if request.method == 'POST':
    photo = request.files['photo']
    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename('temp')))
    
    account = request.form
    username = account['username']
    email = account['email']
    password = account['password']

    mariadb_connect = mariadb.connect(user='root', password='rootpassword', database='Assassins', host='assassins-db', port="3306")
    cur = mariadb_connect.cursor(buffered=True)


    data = cur.execute(f'SELECT * FROM first WHERE email="{email}";')
    try:
      data = cur.fetchone()[3]

      if sha256_crypt.verify(password, data):
        account = True
      else:
        account = False
    except:
      account = False

    if account:
      return redirect('/')
    else:
      cur.execute(f'INSERT INTO first (username, email, password, photo) VALUES (%s, %s, %s, %s)', (username, email, sha256_crypt.hash(password), convertToBinaryData(os.path.join(app.config['UPLOAD_FOLDER'], 'temp'))))
      cur.execute(f'SELECT uid FROM first WHERE password="{sha256_crypt.hash(password)}"')
      session['uid'] = cur.fetchone()
      mariadb_connect.commit()
      cur.close()
    
    return redirect('/')

@app.route('/remove')
def remove():
  mariadb_connect = mariadb.connect(user='root', password='rootpassword', database='Assassins', host='assassins-db', port="3306")
  cur = mariadb_connect.cursor(buffered=True)
  cur.execute(f'DELETE FROM first where email="{session.get("email")}"')
  mariadb_connect.commit()
  cur.close()
  session['logged_in'] = False
  return redirect('/')

@app.route('/logout')
def logout():
  session['logged_in'] = False
  return redirect('/')

if __name__ == "__main__":
  app.secret_key = os.urandom(12)
  app.run(debug=True,host='0.0.0.0', port=5000)
