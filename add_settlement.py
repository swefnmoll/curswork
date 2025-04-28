import sqlite3 as sq

connection = sq.connect('intonation.db')
cursor = connection.cursor()
def add_settlements(settlements):
    # Вставка названий поселений
    for stl in settlements.split(sep='; '):
        cursor.execute(f'''INSERT INTO settlements (settlement) VALUES ('{stl}')''')
        connection.commit()
