from flask import Flask, render_template, request
import sqlite3 as sq
from flask_bootstrap import Bootstrap
from flask_paginate import Pagination, get_page_parameter

# Подключение к БД
connection = sq.connect('intonation.db', check_same_thread=False)
cursor = connection.cursor()

app = Flask(__name__, template_folder='templates')
bootstrap = Bootstrap(app)

@app.route('/search')
def sen_data():

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

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/for_citation')
def for_citation():
    return render_template('for_citation.html')

@app.route('/results', methods=['POST', 'GET'])
def results():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    elem_to_display = 10
    offset = (page - 1) * elem_to_display
    characteristics = {
        'lang' : '%', 'dictor' : '%', 'education' : '%',
        'settlement' : '%', 'gender' : '%', 'age_from' : 0, 'age_to' : 9999}

    # Получение данных из формы
    for char in characteristics.keys():
        req_data = request.form.get(char)
        if req_data:
            characteristics[char] = req_data
    # Поиск по БД
    cursor.execute(f'''
    SELECT files.file, files.text, files.dictor
    FROM files WHERE files.dictor IN (SELECT dictors.name FROM dictors
    INNER JOIN languages ON languages.id = dictors.lang
    INNER JOIN education ON education.id = dictors.education
    INNER JOIN settlements ON settlements.id = dictors.settlement
    WHERE languages.lang LIKE '{characteristics['lang']}'
    AND dictors.name LIKE '{characteristics['dictor']}'
    AND education.level LIKE '{characteristics['education']}'
    AND settlements.settlement LIKE '{characteristics['settlement']}'
    AND dictors.gender LIKE '{characteristics['gender']}'
    AND dictors.DOB >= {characteristics['age_from']}
    AND dictors.DOB <= {characteristics['age_to']})
    ''')
    total = len(cursor.fetchall())

    cursor.execute(f'''
    SELECT files.file, files.text, files.dictor
    FROM files WHERE files.dictor IN (SELECT dictors.name FROM dictors
    INNER JOIN languages ON languages.id = dictors.lang
    INNER JOIN education ON education.id = dictors.education
    INNER JOIN settlements ON settlements.id = dictors.settlement
    WHERE languages.lang LIKE '{characteristics['lang']}'
    AND dictors.name LIKE '{characteristics['dictor']}'
    AND education.level LIKE '{characteristics['education']}'
    AND settlements.settlement LIKE '{characteristics['settlement']}'
    AND dictors.gender LIKE '{characteristics['gender']}'
    AND dictors.DOB >= {characteristics['age_from']}
    AND dictors.DOB <= {characteristics['age_to']})
    LIMIT {elem_to_display} OFFSET {offset}
    ''')
    data = list(cursor.fetchall())
    result = []
    for i, elem in enumerate(data):
        new_elem = list(elem)
        new_elem.append(i)
        result.append(new_elem)
    print(result)
    pagination = Pagination(page=page, page_per=elem_to_display, total=total, prev_label='<', next_label='>', found=total, display_msg='Найдено записей: <b>{found}</b>, показано: <b>{start} - {end}</b>')

    return render_template('search_result.html', result=result, pagination=pagination, css_framework='bootstrap5')

app.run(port=1000, debug=True)
cursor.close()
connection.close()