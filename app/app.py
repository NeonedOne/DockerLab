import time
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, engine
import psycopg2

DBUSER = 'admin'
DBPASS = 'adminadmin'
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'studb'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'adminadmin'


db = SQLAlchemy(app)

def getworst():
  conn = psycopg2.connect(database=DBNAME, user=DBUSER,
                          password=DBPASS, host=DBHOST)
  cursor = conn.cursor()
  #cursor.execute("SELECT *, sum(PE + Physics + Chemistry + Progs) AS total FROM students LIMIT 4;")
  cursor.execute("SELECT * FROM students ORDER BY sum LIMIT 1;")
  #cursor.execute("SELECT * FROM students;")
  results = cursor.fetchall()
  return results

class students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    PE = db.Column(db.Integer)
    Physics = db.Column(db.Integer)
    Chemistry = db.Column(db.Integer)
    Progs = db.Column(db.Integer)
    sum = db.Column(db.Integer)

    def __init__(self, name, PE, Physics, Chemistry, Progs, sum):
        self.name = name
        self.PE = PE
        self.Physics = Physics
        self.Chemistry = Chemistry
        self.Progs = Progs
        self.sum = sum


def dbsequence():
    db.create_all()

    first = students(
            'Poddubniy I.',
            5, 2, 4, 4, 15)
    second = students(
        'Popov A.',
        4, 5, 4, 4, 17)
    third = students(
        'Mendeleev D.',
        3, 5, 5, 4, 17)
    fourth = students(
        'Utukina K.',
        4, 5, 4, 4, 17)
    fifth = students(
        'Briggs V.',
        3, 3, 2, 3, 11)
    db.session.add(first)
    db.session.add(second)
    db.session.add(third)
    db.session.add(fourth)
    db.session.add(fifth)
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def home():
    students = getworst()
    if request.method == 'POST':
        try:
            var = [int(request.form['InputValue']), type(int(request.form['InputValue'])), "SUCCESS"]
        except:
            var = [request.form['InputValue'], type(request.form['InputValue']), "FAILURE"]
        return render_template('page.html', var=var, student=students)

    #return render_template('lab1.html', students=students.query.all())
    return render_template('page.html', student=students)


if __name__ == '__main__':
    dbsequence()
    app.run(debug=True, host='0.0.0.0')
