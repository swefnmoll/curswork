from flask import Flask, request, render_template, make_response
import sqlalchemy as db
from sqlalchemy import create_engine, MetaData

app = Flask(__name__, static_url_path=None)
engine = create_engine('sqlite:///intonation.db')
connection = engine.connect()
metadata = MetaData(bind=engine)
print(metadata.tables['settlements'])

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
    # Поиск по БД

    return render_template('search_result.html', result=data)
app.run(port=1500, debug=True)