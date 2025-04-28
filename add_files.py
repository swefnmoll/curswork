import os
import sqlite3 as sq
from flask import Flask, request, render_template
import mytextgrid as mtg

# Подключение к БД
connection = sq.connect('intonation.db', check_same_thread=False)
cursor = connection.cursor()

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def form_get():
    # Считывание данных из формы
    files = request.files.getlist('files')
    dictor = request.form.get('dictor')[2:-3]

    # Создание директории
    if not os.path.exists('static/' + dictor):
        os.mkdir(dictor)

    def save_file(file):
        file.save(f'static\{dictor}\{filename}')

    # Чтение данных из TextGrid
    def read_data(file):
        global text, cropped_filename
        if filename.endswith('.TextGrid'):
            cropped_filename = filename[:-9]
            tg = mtg.read_from_file(f'static\{dictor}\{filename}')
            for interval in tg.tiers[0]:
                if len(interval.text) > 2:
                    text = interval.text
        return (text, cropped_filename, dictor)

    # Загрузка данных в БД
    def upload_file(data):
        if filename.endswith('.wav'):
            cursor.execute(f'''INSERT INTO files (text, file, dictor)
            VALUES (?, ?, ?)''', data)
            connection.commit()

    # Загрузка всех файлов из формы
    for file in files:
        filename = file.filename
        save_file(file)
        data = read_data(file)
        upload_file(data)


    return render_template('successful_download.html')
app.run(port=2500, debug=True)
cursor.close()
connection.close()