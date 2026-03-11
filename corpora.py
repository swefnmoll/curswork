from flask import Flask, render_template, request
import sqlite3 as sq
from flask_bootstrap import Bootstrap
from flask_paginate import get_page_parameter, Pagination

# Подключение к БД

app = Flask(__name__, template_folder='templates')
bootstrap = Bootstrap(app)

@app.route('/search')
def sen_data():
    connection = sq.connect('intonation.db', check_same_thread=False)
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

    cursor.execute('''SELECT theme FROM themes''')
    themes = list(cursor.fetchall())

    cursor.execute('''SELECT type FROM types''')
    types = list(cursor.fetchall())

    cursor.execute('''SELECT subtype FROM subtypes''')
    subtypes = list(cursor.fetchall())


    # Обрезка строк
    def cut(lst):
        for index, value in enumerate(lst):
            lst[index] = str(value)[2:-3]
    cut(languages)
    cut(levels)
    cut(settlements)
    cut(dictors)
    cut(themes)
    cut(types)
    cut(subtypes)
    cursor.close()
    connection.close()
    return render_template('corpora.html', languages=languages, levels=levels, settlements=settlements, dictors=dictors, themes=themes, types=types, subtypes=subtypes)

@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/info_barab')
def info_barab():
    return render_template('info_barab.html')

@app.route('/info_chat')
def info_chat():
    return render_template('info_chat.html')

@app.route('/info_kumand')
def info_kumand():
    return render_template('info_kumand.html')

@app.route('/info_plautdietsch')
def info_plotd():
    return render_template('info_plotd.html')

@app.route('/info_teleut')
def info_teleut():
    return render_template('info_teleut.html')


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
    connection = sq.connect('intonation.db', check_same_thread=False)
    cursor = connection.cursor()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    elem_to_display = 10
    offset = (page - 1) * elem_to_display

    if request.args.get('lang'):
        lang = request.args.get('lang')
    else:
        lang = '%'
    if request.args.get('type'):
        type = request.args.get('type')
    else:
        type = '%'
    if request.args.get('subtype'):
        subtype = request.args.get('subtype')
    else:
        subtype = '%'
    if request.args.get('education'):
        education = request.args.get('education')
    else:
        education = '%'
    if request.args.get('settlement'):
        settlement = request.args.get('settlement')
    else:
        settlement = '%'
    if request.args.get('gender'):
        gender = request.args.get('gender')
    else:
        gender = '%'
    if request.args.get('dictor'):
        dictor = request.args.get('dictor')
    else:
        dictor = '%'
    if request.args.get('age_from'):
        age_from = request.args.get('age_from')
    else:
        age_from = 0
    if request.args.get('age_to'):
        age_to = request.args.get('age_to')
    else:
        age_to = 9999


    # Получение данных из формы

    print('l::' + lang)

    # Поиск по БД
    cursor.execute(f'''
    SELECT files.file, files.text, files.translation, files.dictor
    FROM files WHERE files.dictor IN (SELECT dictors.name FROM dictors
    INNER JOIN languages ON languages.id = dictors.lang
    INNER JOIN education ON education.id = dictors.education
    INNER JOIN settlements ON settlements.id = dictors.settlement
    WHERE languages.lang LIKE '{lang}'
    AND dictors.name LIKE '{dictor}'
    AND education.level LIKE '{education}'
    AND settlements.settlement LIKE '{settlement}'
    AND dictors.gender LIKE '{gender}'
    AND dictors.DOB >= {age_from}
    AND dictors.DOB <= {age_to})
    AND files.type LIKE '{type}'
    AND files.subtype LIKE '{subtype}'
    ORDER BY files.file ASC''')
    total = len(cursor.fetchall())

    cursor.execute(f'''
    SELECT files.file, files.text, files.translation, files.dictor
    FROM files WHERE files.dictor IN (SELECT dictors.name FROM dictors
    INNER JOIN languages ON languages.id = dictors.lang
    INNER JOIN education ON education.id = dictors.education
    INNER JOIN settlements ON settlements.id = dictors.settlement
    WHERE languages.lang LIKE '{lang}'
    AND dictors.name LIKE '{dictor}'
    AND education.level LIKE '{education}'
    AND settlements.settlement LIKE '{settlement}'
    AND dictors.gender LIKE '{gender}'
    AND dictors.DOB >= {age_from}
    AND dictors.DOB <= {age_to})
    AND files.type LIKE '{type}'
    AND files.subtype LIKE '{subtype}'
    ORDER BY files.file ASC
    LIMIT {elem_to_display} OFFSET {offset}
    ''')
    data = list(cursor.fetchall())
    result = []
    for i, elem in enumerate(data):
        new_elem = list(elem)
        new_elem.append(i)
        result.append(new_elem)
    pagination = Pagination(page=page, page_per=elem_to_display, total=total, offset=offset, prev_label='<', next_label='>', bs_version=5)
    cursor.close()
    connection.close()
    return render_template('search_result.html', result=result, pagination=pagination, css_framework='bootstrap5')

@app.route('/results_dialogs', methods=['POST', 'GET'])
def results_dialogs():
    connection = sq.connect('intonation.db', check_same_thread=False)
    cursor = connection.cursor()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    elem_to_display = 10
    offset = (page - 1) * elem_to_display

    if request.args.get('lang'):
        lang = request.args.get('lang')
    else:
        lang = '%'
    if request.args.get('theme'):
        theme = request.args.get('theme')
    else:
        theme = '%'
    # Поиск по БД
    cursor.execute(
    f'''
    SELECT full_dialogs.id, languages.lang, themes.theme
    FROM full_dialogs
    INNER JOIN languages ON languages.id = full_dialogs.lang 
    INNER JOIN themes ON themes.id = full_dialogs.theme
    WHERE languages.lang LIKE '{lang}'
    AND themes.theme LIKE '{theme}'
    ORDER BY full_dialogs.id ASC
    ''')

    total = len(cursor.fetchall())

    cursor.execute(
    f'''
    SELECT full_dialogs.id, languages.lang, themes.theme
    FROM full_dialogs
    INNER JOIN languages ON languages.id = full_dialogs.lang 
    INNER JOIN themes ON themes.id = full_dialogs.theme
    WHERE languages.lang LIKE '{lang}'
    AND themes.theme LIKE '{theme}'
    ORDER BY full_dialogs.id ASC
    LIMIT {elem_to_display} OFFSET {offset}
    ''')

    data = list(cursor.fetchall())
    
    def read_text_and_tranls(id):
        with open(f'static/full_dialogs/texts/{id}.txt', 'r', encoding='utf-8') as file:
            text = file.read().splitlines()
        with open(f'static/full_dialogs/translations/{id}.txt', 'r', encoding='utf-8') as file:
            transl = file.read().splitlines()
        return text, transl
    
    result = []
    for i, elem in enumerate(data):
        new_elem = list(elem[1:]) + list(read_text_and_tranls(elem[0]))
        new_elem.append(i)
        new_elem.append(str(elem[0]))
        print(len(new_elem))
        if len(new_elem) > 6:
            print(new_elem)
        result.append(new_elem)
    pagination = Pagination(page=page, page_per=elem_to_display, total=total, offset=offset, prev_label='<', next_label='>')
    cursor.close()
    connection.close()
    return render_template('result_dialogs.html', result=result, pagination=pagination, css_framework='bootstrap5')
app.run(port=4444, debug=True)
cursor.close()
connection.close()