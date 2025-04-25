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
    lang = request.form.get('lang')
    dictor = request.form.get('dictor')
    education = request.form.get('education')
    settlement = request.form.get('settlement')
    gender = request.form.get('gender')
    age_from = request.form.get('age_from')
    age_to = request.form.get('age_to')
    if lang == '-':
        lang = '%'
    if dictor == '-':
        dictor = '%'
    if education == '-':
        education = '%'
    if settlement == '-':
        settlement = '%'
    if gender == '-':
        gender = '%'
    if age_from == '':
        age_from = 0
    else:
        age_from = int(age_from)
    if age_to == '':
        age_to = 9999
    else:
        age_to = int(age_to)
    cursor.execute(f'''
    SELECT file, text, dictor FROM files WHERE
    dictor IN (SELECT name FROM dictors
    INNER JOIN languages ON dictors.lang = languages.id 
    INNER JOIN education ON dictors.education = education.id
    INNER JOIN settlements ON dictors.settlement = settlements.id
    AND dictors.name LIKE'{dictor}'
    AND dictors.gender LIKE '{gender}'
    AND languages.lang LIKE '{lang}'
    AND education.level LIKE '{education}'
    AND settlements.settlement LIKE '{settlement}'
    AND dictors.DOB >= {age_from}
    AND dictors.DOB <= {age_to})
    ''')

    raw_data = list(cursor.fetchall())
    for value, item in enumerate(raw_data):
        raw_data[value] = list(item)
    for elem in raw_data:
        files.append(elem[2] + '/' + elem[0] + '.wav')
        texts.append(elem[1])
        dictors.append(elem[2])
    return render_template('search_result.html', result=zip(files, dictors, texts))

app.run(port=1500, debug=True)
cursor.close()
connection.close()