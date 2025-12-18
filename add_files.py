import pathlib

import numpy as np
import sqlite3 as sq
from flask import Flask, request, render_template
import mytextgrid as mtg
import parselmouth
import matplotlib.pyplot as plt
from annotation import Annotation
from os import path

# Подключение к БД
connection = sq.connect('intonation.db', check_same_thread=False)
cursor = connection.cursor()

app = Flask(__name__)

class AddedFile:

    def __init__(self, file):
        cursor.execute('''SELECT MAX(`id`) FROM files''')
        raw_max_id = cursor.fetchall()[0][0]
        max_id = 0 if raw_max_id is None else raw_max_id
        self.filename = str(max_id + 1) + path.splitext(file.filename)[1]
        self.path = fr'static\audio\{self.filename}'
        file.save(self.path)
        self.tg = mtg.read_from_file(pathlib.PurePath(self.path).with_suffix('.TextGrid'))
        if self.filename.endswith('.wav'):
            ann_file = Annotation(self.path)
            ann_file.annotate()
            data = self.read_data()
            self.draw_image()
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
        return cropped_filename, dictor, type, subtype, text, translation

    def read_tg(self):
        syntagms = []
        syllabes = []
        for interval in self.tg.tiers[1]:
            syntagms.append([interval.xmin, interval.text])
        for interval in self.tg.tiers[2]:
            syllabes.append([interval.xmin, interval.text])
        return {'syntagms' : syntagms, 'syllabes': syllabes}

    def read_chars(self):
        snd = parselmouth.Sound(self.path)
        oscillogram = snd
        spectrogram = snd.to_spectrogram()
        pitch = snd.to_pitch()
        intensity = snd.to_intensity()
        syntagms = self.tg.tiers[1]
        syllabes = self.tg.tiers[2]
        return oscillogram, spectrogram, pitch, intensity, syntagms, syllabes

    def draw_image(self):
        chars = self.read_chars()
        plt.subplot(6, 1, 1)
        plt.plot(chars[0].xs(), chars[0].values.T, linewidth=0.2)

        plt.subplot(6, 1, 2)
        x, y = chars[1].x_grid(), chars[1].y_grid()
        sg_db = 10 * np.log10(chars[1].values)
        plt.pcolormesh(x, y, sg_db, vmin=sg_db.max() - 50)
        plt.ylim([chars[1].ymin, chars[1].ymax])
        plt.xlabel("time [s]")
        plt.ylabel("frequency [Hz]")
        plt.subplot(6, 1, 3)
        plt.plot(chars[2].xs(), chars[2].selected_array['frequency'], linewidth=2, color='blue')
        plt.subplot(6, 1, 4)
        plt.plot(chars[3].xs(), chars[3].values.T, linewidth=2, color='green')
        
        textgrid = self.read_tg()
        
        plt.subplot(6, 1, 5)
        syntagm_tier = textgrid['syntagms']
        for syntagm in syntagm_tier:
            plt.axvline(syntagm[0]) 
            plt.text(syntagm[0], 0.5, syntagm[1], fontsize=8)
        
        plt.subplot(6, 1, 6)
        syllabe_tier = textgrid['syllabes']
        for syllabe in syllabe_tier:
            plt.axvline(syllabe[0])
            plt.text(syllabe[0], 0.5, syllabe[1], fontsize=8)
                
        path_to_img = fr'static\images\{self.filename[:-4]}.jpeg'
        print(path_to_img)
        plt.savefig(path_to_img)
        plt.close()

    # Загрузка данных в БД
    def upload_file(self, data):
        if self.filename.endswith('.wav'):
            cursor.execute(f'''INSERT INTO files (file, dictor, type, subtype, text, translation)
            VALUES (?, ?, ?, ?, ?, ?)''', data)
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