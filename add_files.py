import os
import sqlite3 as sq
from flask import Flask, request, render_template
import mytextgrid as mtg
import parselmouth
import matplotlib as mpl
import annotation

# Подключение к БД
connection = sq.connect('intonation.db', check_same_thread=False)
cursor = connection.cursor()

app = Flask(__name__)

class AddedFile:
    def __init__(self, file):
        filename = file.filename
        file.save(f'static\audio\{filename}')
        annotation.read_and_annotate(filename)

    # Чтение данных из TextGrid
    def read_data(file):
        global text, cropped_filename
        if filename.endswith('.TextGrid'):
            cropped_filename = filename[:-9]
            tg = mtg.read_from_file(f'static\{dictor}\{filename}')
            for interval in tg.tiers[0]:
                if len(interval.text) > 2:
                    information = interval.text.split(sep=' // ')
                    text, translation, dictor, type, subtype = information
        return (text, cropped_filename, dictor)

    def read_chars(file):
        snd = parselmouth.Sound(file)
        oscillogram = snd.values.T
        spectrogram = snd.to_spectrogram()
        pitch = snd.to_pitch()
        intensity = snd.to_intensity()
        tg = mtg.read_from_file(file)
        syntagms = tg.tiers[1]
        syllabes = tg.tiers[2]

    def read_syntagms(self, syntagms):

    def draw_image(self):

    # Загрузка данных в БД
    def upload_file(data):
        if filename.endswith('.wav'):
            cursor.execute(f'''INSERT INTO files (text, file, dictor)
            VALUES (?, ?, ?)''', data)
            connection.commit()

@app.route('/', methods=['POST', 'GET'])
def form_get():
    files = request.files.get_list('files')
    # Загрузка всех файлов из формы
    for file in files:
        data = read_data(file)
        upload_file(data)


    return render_template('successful_download.html')
app.run(port=2500, debug=True)
cursor.close()
connection.close()