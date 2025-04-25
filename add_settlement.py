import sqlite3 as sq

connection = sq.connect('intonation.db')
cursor = connection.cursor()

s = input(r'Введите название поселений: ')

for stl in s.split(sep='; '):
    cursor.execute(f'''INSERT INTO settlements (settlement) VALUES ('{stl}')''')
    connection.commit()

cursor.close()
connection.close()