import hashlib 
import os 
import sqlite3 

#Подключение к БД 
connection = sqlite3.connect('DB_U.db') 
cursor = connection.cursor() 

#Инициализация данных пользователя 
username = 'admin' 
password = 'admin' 

#Генерация случайно соли 
salt = os.urandom(32) 

#Вычисление ключа 
key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000) 

#Добавление полученных данных в БД 
cursor.execute('INSERT INTO Users (LOGIN, SALT, KEY) VALUES (?, ?, ?)', (username, salt, key)) 
connection.commit() 

#Проверка результата хеширования 
res = cursor.execute('SELECT SALT,KEY FROM Users WHERE LOGIN = ?', (username,)).fetchall()[0] 
salt = res[0] 
key = res[1] 
print(*key) 
newkey = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000) 
print(*newkey) 
if newkey == key: 
    print('Введённый пароль верный') 
    
connection.close()