  GNU nano 7.2                                                                                                                      flaskapp.py                                                                                                                               from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLite setup
db_path = "/var/www/html/flaskapp/users.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT, password TEXT, firstname TEXT, lastname TEXT, email TEXT)''')
conn.commit()
conn.close()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, firstname, lastname, email) VALUES (?, ?, ?, ?, ?)",
              (username, password, firstname, lastname, email))
    conn.commit()
    conn.close()

    return redirect(url_for('profile', username=username))

@app.route('/profile/<username>')
def profile(username):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()

    return render_template('profile.html', user=user)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password,))
    user = c.fetchone()
    conn.close()

    if user == None:
        return redirect(url_for('login'))

    return redirect(url_for('profile', username=username))

if __name__ == '__main__':
    app.run(debug=True)
