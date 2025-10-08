import pathlib

import numpy as np
import sqlite3 as sq
from flask import Flask, request, render_template
import mytextgrid as mtg
import parselmouth
import matplotlib.pyplot as plt
from annotation import Annotation
from werkzeug.utils import secure_filename

# Подключение к БД
connection = sq.connect('intonation.db', check_same_thread=False)
cursor = connection.cursor()

app = Flask(__name__)

class AddedFile:

    def __init__(self, file):
        self.s_filename = secure_filename(file.filename)
        self.filename = fr'static\audio\{self.s_filename}'
        file.save(fr'static\audio\{secure_filename(file.filename)}')
        if self.filename.endswith('.wav'):
            ann_file = Annotation(self.filename)
            ann_file.annotate()
            self.draw_image()
            data = self.read_data()
            self.upload_file(data)

    # Чтение данных из TextGrid
    def read_data(self):
        cropped_filename = self.filename[:-4]
        for interval in self.tg.tiers[0]:
            if len(interval.text) > 1:
                information = interval.text.split(sep='//')
                print(information)
                information = list(map(lambda x: x.strip(), information))
                text, translation, dictor, type, subtype = information
                break
        return cropped_filename, text, translation, dictor, type, subtype

    def read_chars(self):
        snd = parselmouth.Sound(self.filename)
        oscillogram = snd
        spectrogram = snd.to_spectrogram()
        pitch = snd.to_pitch()
        intensity = snd.to_intensity()
        self.tg = mtg.read_from_file(pathlib.PurePath(self.filename).with_suffix('.TextGrid'))
        syntagms = self.tg.tiers[1]
        syllabes = self.tg.tiers[2]
        return oscillogram, spectrogram, pitch, intensity, syntagms, syllabes

    def draw_image(self):
        chars = self.read_chars()
        plt.subplot(3, 1, 1)
        plt.plot(chars[0].xs(), chars[0].values.T)

        plt.subplot(3, 1, 2)
        x, y = chars[1].x_grid(), chars[1].y_grid()
        sg_db = 10 * np.log10(chars[1].values)
        plt.pcolormesh(x, y, sg_db, vmin=sg_db.max() - 50)
        plt.ylim([chars[1].ymin, chars[1].ymax])
        plt.xlabel("time [s]")
        plt.ylabel("frequency [Hz]")
        plt.plot(chars[2].xs(), chars[2].selected_array['frequency'], linewidth=3, color='blue')
        plt.plot(chars[3].xs(), chars[3].values.T, linewidth=3, color='green')

        path_to_img = fr'static\images\{self.s_filename[:-4]}.jpeg'
        print(path_to_img)
        plt.savefig(path_to_img)
        plt.close()

    # Загрузка данных в БД
    def upload_file(self, data):
        if self.filename.endswith('.wav'):
            cursor.executescript(f'''INSERT INTO files (file, dictor, type, subtype, text, translation)
            VALUES (?, ?, ?, ?, ?, ?);
            
            
            
            ''', data)
            connection.commit()

@app.route('/', methods=['POST', 'GET'])
def form_get():
    files = request.files.getlist('files')
    # Загрузка всех файлов из формы
    for file in files:
        added_file = AddedFile(file)
    return render_template('successful_download.html')
app.run(port=2500, debug=True)
cursor.close()
connection.close()