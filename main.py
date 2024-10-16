from flask import Flask, render_template, request, redirect, url_for 
import sqlite3 
import hashlib 
import pandas as pd 
import tensorflow as tf 
import joblib 
import sklearn 

#Переменные инициализации приложения, проверки входа и роли 
app = Flask(__name__) 
enter = False 
username = "" 

#Функция главной страницы 
@app.route('/login',methods=['POST','GET']) 
def login(): 
    error = None 
    global enter 
    global username 
    if request.method == 'POST': 
        username = request.form['username'] 
        password = request.form['password'] 
        
        #Подключение к БД и проверка введённых в форму данных 
        try: 
            connection = sqlite3.connect('DB_U.db') 
            cursor = connection.cursor() 
            res = cursor.execute('SELECT SALT,KEY FROM Users WHERE LOGIN = ?', (username,)).fetchall()[0] 
            salt = res[0] 
            key = res[1] 
            connection.close() 
            newkey = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000) 
            
            #Сравнение хеш-ключей 
            if newkey == key: 
                enter = True 
                return redirect(url_for('stend')) 
            else: error = 'Неправильные данные для входа' 
        except: error = 'Неправильные данные для входа' 
            return render_template('index.html', error=error) 
            
#Функция страницы стенда 
@app.route('/stend',methods=['POST','GET']) 
def stend(): 
    result = 0 
    users="" 
    global enter 
    global username 
    
    #Проверка роли администратора 
    if username == "admin": 
        connection = sqlite3.connect('DB_U.db') 
        cursor = connection.cursor() 
        users = cursor.execute('SELECT LOGIN FROM Users').fetchall() 
        #Проверка входа на главной странице 
        if not enter:
            return redirect(url_for('login')) 
        if request.method == 'POST': 
            #Отправка данных из форм в функция прогнозирования 
            result = predict(request.form['res'],request.form['mat'],re-quest.form['spl'], request.form['grease'],request.form['maxd']) 
        return render_template('stend.html',result=result, users=users) 
        
#Функция перенаправления на страницу логирования 
@app.route('/') 
def main(): 
    return redirect(url_for('login')) 
    
#Функция предсказания 
def predict(res, material, splav, grease, maxd): 
    #Обработка входных данных 
    input_data = pd.DataFrame({ 'grease': [grease], 'maxd': [float(maxd)] }) 
    
    #Инициализация пути к файлу модели 
    model_root = f'./models/{res}/{res}_{material}_{splav}.h5' 
    
    #Подключение модели и препроцессора 
    model = tf.keras.models.load_model(model_root) 
    preprocessor = joblib.load(f'./preprocessors/{material}.pkl') 
    input_processed = preprocessor.transform(input_data) 
    
    #Получение прогноза и его отправка 
    prediction = model.predict(input_processed) 
    return f'Предсказанное значение: {round(float(prediction[0][0]),2)} м/мин'
    
#Запуск веб-приложения 
if __name__ == '__main__': 
    app.run()