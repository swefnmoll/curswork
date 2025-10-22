import sqlite3 as sq
from flask import Flask, request, render_template, make_response

connection = sq.connect('intonation.db', check_same_thread=False)
cursor = connection.cursor()

app = Flask(__name__, static_url_path=None)

@app.route('/', methods=['POST', 'GET'])
def result():
    files = []
    dictors = []
    texts = []
    characteristics = {
        'lang' : '%', 'dictor' : '%', 'education' : '%',
        'settlement' : '%', 'gender' : '%', 'age_from' : 0, 'age_to' : 9999}

    # Получение данных из формы
    for char in characteristics.keys():
        req_data = request.form.get(char)
        if req_data != '':
            characteristics[char] = req_data
    print(characteristics)
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
    data = list(cursor.fetchall())
    return render_template('search_result.html', result=data)
app.run(port=1500, debug=True)
cursor.close()
connection.close()