import sqlite3 as sq
from add_settlement import add_settlements

connection = sq.connect('intonation.db')
cursor = connection.cursor()

# Создание базы данных
def create_db():
    cursor.executescript('''CREATE TABLE IF NOT EXISTS languages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lang TEXT
    );
    
    
    CREATE TABLE IF NOT EXISTS education (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    level TEXT
    );
    
    CREATE TABLE IF NOT EXISTS settlements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    settlement TEXT
    );
    
    CREATE TABLE IF NOT EXISTS dictors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    lang TEXT,
    gender TEXT,
    DOB INTEGER,
    settlement TEXT,
    education TEXT,
    CHECK (gender = 'м' or gender = 'ж'),
    FOREIGN KEY (lang) REFERENCES languages (id),
    FOREIGN KEY (settlement) REFERENCES settlements (id),
    FOREIGN KEY (education) REFERENCES education (id),
    FOREIGN KEY (lang) REFERENCES languages (id)
    );
    
    CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file TEXT,
    dictor INTEGER,
    type INTEGER,
    subtype INTEGER,
    text TEXT,
    translation TEXT,
    FOREIGN KEY (dictor) REFERENCES dictors (id),
    FOREIGN KEY (type) REFERENCES types (id),
    FOREIGN KEY (subtype) REFERENCES subtypes (id)
    );
    
    CREATE TABLE IF NOT EXISTS types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT
    );
    
    CREATE TABLE IF NOT EXISTS subtypes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subtype TEXT
    )
    
    ''')

    connection.commit()

    # Вставка постоянных значений в таблицы

    cursor.executescript('''
    INSERT INTO languages (lang) VALUES ('барабинский'), ('кумандинский'), ('плотдич'), ('телеутский'), ('чатский');
    INSERT INTO education (level) VALUES ('начальное'), ('неполное среднее'), ('полное среднее'), ('среднеспециальное'), ('высшее');
    INSERT INTO types (type) VALUES ('утверждение'), ('вопрос'), ('смеш.'), ('межд.'), ('маркер ОС');
    INSERT INTO subtypes (subtype) VALUES ('информативное'), ('верификативное'), ('инф.+вер.'), ('диктальный'), ('модальный'), ('принятие'), ('подтверждение'), ('внимание')
    ''')
    connection.commit()

create_db()
add_settlements('аул Шагир Куйбышевского района НСО; аул Тармакуль Чановского района НСО; дер. Юрт-Ора Колыванского района НСО; дер.Букачак, Красногорского р-на Алтайского края')