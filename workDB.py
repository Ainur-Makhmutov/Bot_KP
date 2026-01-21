import sqlite3

# Создаем подключение к базе данных
connection = sqlite3.connect('Dungeon_Crusher_Database.db')

connection.close()
