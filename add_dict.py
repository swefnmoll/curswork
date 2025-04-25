import sqlite3 as sq
import openpyxl as xl

connection = sq.connect('intonation.db')
cursor = connection.cursor()

wb = xl.load_workbook('dictors.xlsx')
sh = wb.active

for row in range(1, sh.max_row + 1):
    name = sh.cell(row=row, column=1).value
    gender = sh.cell(row=row, column=2).value
    dob = sh.cell(row=row, column=3).value
    lang = sh.cell(row=row, column=4).value
    settlement = sh.cell(row=row, column=5).value
    education = sh.cell(row=row, column=6).value
    print(name)
    cursor.execute(f'''INSERT INTO dictors (name, gender, DOB, lang, settlement, education) VALUES ('{name}', '{gender}', '{dob}', '{lang}', '{settlement}', '{education}');''')
    connection.commit()
cursor.close()
connection.close()