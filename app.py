from flask import Flask, render_template
import sqlite3 as sq

app = Flask(__name__, template_folder='templates')

# Считывание имён дикторов из БД
@app.route('/')
def sen_data():
    connection = sq.connect('intonation.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT name FROM dictors''')
    dictors = list(cursor.fetchall())
    return render_template('add_files.html', dictors=dictors)
app.run(port=2000, debug=True)