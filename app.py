import flask
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__)
# =======================================================================

@app.route('/')
def index():
    conn = get_db_connection()
    conn.execute('INSERT INTO posts (Name, Staff_member, Rank) VALUES ("List of crew members is here", " ", " ")')
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.before_request
def before_request():
    init_db()

def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT NOT NULL, Staff_member TEXT NOT NULL, Rank TEXT NOT NULL)')
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('baseDB.db')
    conn.row_factory = sqlite3.Row
    return conn

def close_db_connection(conn):
    conn.close()

@app.route('/<int:post_id>')
def get_post(post_id):
    conn = get_db_connection()

    conn.execute('INSERT INTO posts (Name, Staff_member, Rank) VALUES ("List of crew members is here", "potential members of the crues:", " first pylot, second pylot, navigator, flight mechanic")')

    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()


    return render_template('post.html', post = post)

@app.route('/add_post', methods=['GET', 'POST'])
def add_post():


    if request.method == 'POST':

        Name = request.form['Name']
        Staff_member = request.form['Staff_member']
        Rank = request.form['Rank']

        XXXcheckValues = request.form.get('XXXcheckGo')
        XXXcheck = str(XXXcheckValues)

        checkValues = request.form.get('checkGo')
        check = str(checkValues)

        if check == '':
            check = 'exam passed'
        else:
            check = 'exam failed'

        if XXXcheck == '':
            XXXcheck = 'cleared for flights'
        else:
            XXXcheck = 'not allowed to fly'


        Name = Name + '  >'+ check + '  :' + XXXcheck

        conn = get_db_connection()
        conn.execute('INSERT INTO posts (Name, Staff_member, Rank) VALUES (?, ?, ?)', (Name, Staff_member, Rank))

        conn.commit()
        conn.close()

        return redirect(url_for('index'))


    return render_template('add_post.html')


@app.route('/')
@app.route('/sun_system')
def sun_system():

    user = {'nickname': 'Sun System'}

    posts = [
         {'planet':{'nickname':'Sun'},
          'body' : 'stars group'},
        # ===============================

           {'planet':{'nickname':'Mercury'},
            'body' : 'earth group'},
           {'planet':{'nickname':'Venus'},
            'body': 'earth group'},
           {'planet':{'nickname':'Terra'},
            'body': 'earth group'},
           {'planet': {'nickname': 'Mars'},
            'body': 'earth group'},
           {'planet': {'nickname': "Jupiter"},
            'body': 'giants group'},
           {'planet':{'nickname':'Saturn'},
            'body': 'giants group'},
           {'planet': {'nickname':'Uranus'},
            'body': 'giants group'},
           {'planet': {'nickname':'Neptune'},
            'body': 'giants group'},
           {'planet':{'nickname':'Pluto'},
            'body': 'pluto group'},
          ]

    return render_template(
            "sun_system.html",
            title='Home',
            user=user,
            posts=posts
            )


if __name__ == '__main__':
    app.run(debug=True)
