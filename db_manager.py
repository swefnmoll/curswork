from create_db import create_db, connection
from add_dict import read_dictors
from add_settlement import add_settlements
import sqlite3 as sq

command = ''

connection = sq.connect('intonation.db')
cursor = connection.cursor()

while command != 'end':
    command = input('Введите команду: ')
    if command == 'create':
        create_db()
        read_dictors()
        add_settlements(settlements='аул Шагир Куйбышевского района НСО; аул Тармакуль Чановского района НСО; дер. Юрт-Ора Колыванского района НСО; дер.Букачак, Красногорского р-на Алтайского края')