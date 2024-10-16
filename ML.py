import os 
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0' 

import pandas as pd 
from sklearn.preprocessing import OneHotEncoder 
from sklearn.compose import ColumnTransformer 
from sklearn.model_selection import train_test_split 
import keras 
from sklearn.metrics import mean_squared_error 
import joblib 
#Подключение к csv таблице 
data = pd.read_csv('./data/str/str_st_1020.csv',sep=';') 

#Определение входных и выходных данных 
X = data.drop('speed', axis=1) 
y = data['speed'] 
categorical_features = ['grease'] 
numeric_features = ['maxd'] 

#Обработка входных данных 
preprocessor = ColumnTransformer(
    transformers=[ ('num', 'passthrough', numeric_features),
                  ('cat', OneHotEncoder(), categorical_features) ]) 

X_processed = preprocessor.fit_transform(X) 

#Разделение данных на тестовую и обучающую части 
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.05, random_state=0)

#Инициализация НС и её обучение 
model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', in-put_shape=(X_train.shape[1],)),
    keras.layers.Dense(32, activation='relu'), keras.layers.Dense(1)
    ])

model.compile(optimizer='adam', loss='mean_squared_error') 
history = model.fit(X_train, y_train, epochs=800, validation_split=0.15, batch_size=32) 

#Провека среднеквадратичной ошибки
y_pred = model.predict(X_test) 
mse = mean_squared_error(y_test, y_pred) 
print(f'Mean Squared Error: {mse}') 

#Сохранение модели и препроцессора 
model.save('./models/str/str_st_1.h5') 
joblib.dump(preprocessor, './preprocessors/sp.pkl')