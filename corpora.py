from flask import Flask, render_template
import sqlite3 as sq

app = Flask(__name__, template_folder='templates')

@app.route('/search')
def sen_data():
    # Подключение к БД
    connection = sq.connect('intonation.db')
    cursor = connection.cursor()
    # Считывание данных из БД
    cursor.execute('''SELECT lang FROM languages''')
    languages = list(cursor.fetchall())

    cursor.execute('''SELECT level FROM education''')
    levels = list(cursor.fetchall())

    cursor.execute('''SELECT settlement FROM settlements''')
    settlements = list(cursor.fetchall())

    cursor.execute('''SELECT name FROM dictors''')
    dictors = list(cursor.fetchall())

    # Обрезка строк
    def cut(lst):
        for index, value in enumerate(lst):
            lst[index] = str(value)[2:-3]
    cut(languages)
    cut(levels)
    cut(settlements)
    cut(dictors)
    return render_template('corpora.html', languages=languages, levels=levels, settlements=settlements, dictors=dictors)

@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/methods')
def methods():
    return render_template('methods.html')

@app.route('/authors')
def authors():
    return render_template('authors.html')

app.run(port=1000, debug=True)