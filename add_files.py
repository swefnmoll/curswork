import os
import sqlite3 as sq
from flask import Flask, request, render_template
import mytextgrid as mtg

connection = sq.connect('intonation.db', check_same_thread=False)
cursor = connection.cursor()

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def form_get():
    files = request.files.getlist('files')
    dictor = request.form.get('dictor')[2:-3]
    if not os.path.exists(dictor):
        os.mkdir(dictor)
    for file in files:
        file.save(fr'static\{dictor}\{file.filename}')
        if file.filename.endswith('.TextGrid'):
            print(file.filename)
            tg = mtg.read_from_file(fr'static\{dictor}\{file.filename}')
            for interval in tg.tiers[0]:
                if len(interval.text) > 2:
                    text = interval.text
            cursor.executescript(f'''INSERT INTO files (file, dictor, text) VALUES ('{file.filename[:-9]}', '{dictor}', '{text}')''')
            connection.commit()
    return render_template('successful_download.html')
app.run(port=2500, debug=True)
cursor.close()
connection.close()