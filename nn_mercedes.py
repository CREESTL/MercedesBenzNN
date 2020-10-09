# -*- coding: utf-8 -*-
"""NN Mercedes

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hizyc49mkGAWqPkJOHOoq43aC3cizi5F

TO-DO

1) Посмтроить гистограмму истинных Y, посмотреть, номральное ли у них распределение

2) Добавить Dropout

УСТАНОВКА ВСЕХ НЕОБХОДИМЫХ ЗАВИСИМОСТЕЙ
"""

!pip install -U keras-tuner

import pandas as pd
import numpy as np
from keras.datasets import boston_housing
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD
from kerastuner.tuners import RandomSearch, Hyperband, BayesianOptimization
from kerastuner.engine import hyperparameters
from keras.layers import Dropout
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import time
import math
import matplotlib.pyplot as plt
from keras import utils

"""ЧТЕНИЕ И ВЫВОД ИСХОДНЫХ ДАННЫХ"""

TRAIN_FILE_PATH = '/content/drive/My Drive/Интеллектуальный анализ данных ЛР№1/train.csv'

# загружаем данные
x = pd.read_csv(TRAIN_FILE_PATH) 

x

"""ПОЛУЧЕНИЕ ЗНАЧЕНИЙ Y"""

# функция извлекает правильные значение из тренировочных данных
def get_truth(array):
  data = []
  for col_name, col_info in array.items():
    # находится столбец y
    if col_name == "y":
      # все данные из него пререписываются в массив
      for line_number, line_info in col_info.items():
        temp_array = []
        temp_array.append(line_info)
        data.append(temp_array)
  # массив трансформируется в numpy и меняется его размерность
  return np.array(data, dtype=np.float64).reshape(array.shape[0], 1)


y = get_truth(x)
y

"""УДАЛЕНИЕ ЛИШНИХ СТОЛБЦОВ"""

# столбцы 'y' и 'ID' не нужны при работе больше
x.drop('y', axis='columns', inplace=True)
x.drop('ID', axis='columns', inplace=True)
x

"""ШИФРОВАНИЕ ВСЕХ БУКВ И ЦИФР С ПОМОЩЬЮ LABELENCODER"""

# все буквы и цифры шифруются, чтобы остались только числа
df = pd.DataFrame(x)
x = df.apply(preprocessing.LabelEncoder().fit_transform)

x

"""НОРМАЛИЗАЦИЯ ДАННЫХ"""

# функция нормализуем данные для работы
def normalize_data(data):
  mean = data.mean(axis=0)
  std = data.std(axis=0)
  data -= mean
  data /= std
  return data

  
x_norm = normalize_data(x)
x_norm

"""ПРОВЕРКА НА НАЛИЧИЕ NaN"""

def check_nans(data):
  # массив названий столбцов, в которых одни NaN
  nan_cols = []
  for col_name, col_info in data.items():
    for line_number, line_info in col_info.items():
      if math.isnan(line_info):
        print(f"{col_name } is NaNs")
        nan_cols.append(col_name)
        break
  if nan_cols == []:
    print("[INFO] THERE IS NO NaNS IN DATA!")
  return nan_cols

nan_cols = check_nans(x_norm)

"""УДАЛЕНИЕ ВСЕХ СТОЛБЦОВ С NaN"""

def delete_nans(data, nan_cols):
  for col in nan_cols:
    try:
      x.drop(str(col), axis='columns', inplace=True)
    except:
      continue

delete_nans(x_norm, nan_cols)

"""ПОВТОРНАЯ ПРОВЕРКА НА NaN"""

check_nans(x_norm)

"""ДЕЛИМ ДАННЫЕ НА ТРЕНИРОВОЧНЫЕ И ТЕСТОВЫЕ В СООТНОШЕНИИ 70/30"""

# делим в соотношении 70 на 30
(x_train, x_test) = train_test_split(x_norm, test_size=0.3)
(y_train, y_test) = train_test_split(y, test_size=0.3)

"""ПРЕОБРАЗОВАНИЕ ВСЕХ ДАННЫХ В NUMPY"""

# функция принимает данные, прочитанные из csv файла, переводит их в numpy_array
def convert_csv_to_numpy(array):
  array_to_convert = []
  for col_name, col_info in array.items():
    # временный массив создается для каждого СТОЛБЦА
    temp_array = []
    for line_number, line_info in col_info.items():
        temp_array.append(line_info)
    # после прохождения всего столбца временный массив добавляется в основной
    if temp_array != []:
      array_to_convert.append(temp_array)
  # в самом конце основном массив конвертируется в numpy_array
  return np.array(array_to_convert, dtype=np.float64)


x_train = convert_csv_to_numpy(x_train) 
x_test = convert_csv_to_numpy(x_test)

x_train

x_test

"""ИЗМЕНЕНИЕ ФОРМЫ ТЕНЗОРОВ"""

# меняю формы обоих x, чтобы первое измерение совпадало с y
x_train = np.reshape(x_train, (x_train.shape[1], x_train.shape[0]))
x_test = np.reshape(x_test, (x_test.shape[1], x_test.shape[0]))

print(f"Y_TRAIN SHAPE IS {y_train.shape}")
print(f"Y_TEST SHAPE IS {y_test.shape}")
print(f"X_TRAIN SHAPE IS {x_train.shape}")
print(f"X_TEST SHAPE IS {x_test.shape}")
print("\n\n")

"""БЕРЕМ 30 ПРОЦЕНТОВ ТРЕНИРОВОЧНЫХ ДАННЫХ ДЛЯ ПРОВЕРКИ **ВО ВРЕМЯ ТРЕНИРОВКИ**"""

(x_train_main, x_train_val) = train_test_split(x_train, test_size=0.3)
(y_train_main, y_train_val) = train_test_split(y_train, test_size=0.3)

"""СОЗДАНИЕ И ОБУЧЕНИЕ МОДЕЛИ ВРУЧНУЮ (ПОКА ЧТО ЛУЧШИЙ ВАРИАНТ)"""

model = Sequential()
model.add(Dense(1024, activation="relu", input_shape=(x_train_main.shape[1],)))
model.add(Dense(512, activation="relu"))
model.add(Dense(1))
print("[INFO] NN has been created")
model.compile(optimizer="rmsprop", loss="mse", metrics=["mae"])
print("[INFO] NN has been compiled")
model.summary()
# начинаем обучение нейронной сети
history = model.fit(x_train_main, y_train_main, epochs=100, batch_size=100, validation_data=(x_train_val, y_train_val))
history = history.history
print("[INFO] Training has been finished")

model = Sequential()
model.add(Dense(1024, activation="relu", input_shape=(x_train_main.shape[1],)))
model.add(Dense(512, activation="relu"))
model.add(Dropout(0.2))
model.add(Dense(1))
print("[INFO] NN has been created")
model.compile(optimizer="rmsprop", loss="mse", metrics=["mae"])
print("[INFO] NN has been compiled")
model.summary()
# начинаем обучение нейронной сети
history = model.fit(x_train_main, y_train_main, epochs=100, batch_size=100, validation_data=(x_train_val, y_train_val))
history = history.history
print("[INFO] Training has been finished")

"""СОЗДАНИЕ ГРАФИКОВ"""

# функция строит графики после тренировки
def draw_graph(history):
    loss_values = history["loss"]
    validation_loss_values = history["val_loss"]

    epochs = range(1, len(history['loss']) + 1)

    #               ГРАФИКИ ПОТЕРЬ
    # синими точками рисуется график потерь на этапе обучения
    plt.plot(epochs, loss_values, 'or', label='Training loss')
    # синей линией рисуется график потерь на этапе проверки
    plt.plot(epochs, validation_loss_values, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    # очищаем рисунок
    plt.clf()

    #               ГРАФИКИ ОШИБКИ
    acc_values = history['mae']
    validation_acc_values = history['val_mae']
    plt.plot(epochs, acc_values, 'or', label='Training mae')
    plt.plot(epochs, validation_acc_values, 'b', label='Validation mae')
    plt.title('Training and validation mae')
    plt.xlabel('Epochs')
    plt.ylabel('mae')
    plt.legend()
    plt.show()



# рисуем все графики
draw_graph(history)

"""ВЫЧИСЛЕНИЕ ОШИБКИ ТРЕНИРОВКИ"""

print("[INFO] RUNNING ON TEST DATA: \n")
# вычисляем ошибки и выводим их на экран
mse, mae = model.evaluate(x_test, y_test, verbose=1)
print(f"[INFO] Mean squared error is {mse}")
print(f"[INFO] Mean absolute error is {mae}")

"""СОЗДАНИЕ И ОБУЧЕНИЕ МОДЕЛИ ЧЕРЕЗ KERAS TUNER"""

# функция создание нейронной сети
def build_NN(hp):
  model = Sequential()
  # варианты активационых функций
  activation_choice = hp.Choice("activation", values=["relu", "tanh"])
  # создаем один входной слой
  model.add(Dense(units=hp.Int("units_input", min_value=4,max_value=128, step=32), activation=activation_choice, input_dim=364))
  # опционально добавляются еще слои разной конфигурации
  for i in range(hp.Int("n_layers", 2, 3)):
    model.add(Dense(units=hp.Int("units_"+str(i), min_value=4, max_value=128, step=32), activation=activation_choice))
  # создаем один выходной слой
  model.add(Dense(1))
  # компиляция сети происходит с выборо одного из оптимизаторов
  model.compile(optimizer=hp.Choice("optimizer", values=["rmsprop"]), loss="mse", metrics=["mae"])
  model.summary()
  return model


def find_best_NN(x_train_main, y_train_main):
  # создаю тюнер, который сможет подобрать оптимальную архитектуру модели
  tuner = RandomSearch(build_NN, objective="loss", max_trials=20, executions_per_trial=1)
  print("\n\n\n")
  # начинается автоматический подбор гиперпараметров
  print('[INFO] start searching')
  tuner.search(x_train_main, y_train_main, batch_size=100, epochs=10, validation_data=(x_train_val, y_train_val))
  # выбираем лучшую модель
  print("\n\n\nRESULTS SUMMARY")
  tuner.results_summary()
  print("\n\n\n")
  # получаем лучшую модель
  print("\n\n\nHERE IS THE BEST MODEL\n\n\n")
  best_model = tuner.get_best_models(num_models=1)[0]

  return best_model
  

best_model = find_best_NN(x_train_main, y_train_main)

"""ТРЕНИРОВКА НАИЛУЧШЕЙ МОДЕЛИ"""

best_history = best_model.fit(x_train_main, y_train_main, epochs=30, batch_size=100, validation_data=(x_train_val, y_train_val))
best_history = best_history.history
print("[INFO] Training has been finished")

"""ГРАФИКИ ТРЕНИРОВКИ ЛУЧШЕЙ МОДЕЛИ"""

# рисуем все графики
draw_graph(best_history)

"""ПРОВЕРКА ЛУЧШЕЙ МОДЕЛИ НА ТЕСТОВЫХ ДАННЫХ"""

mse, mae = best_model.evaluate(x_test, y_test, verbose=1)
print(f"[INFO] Mean squared error is {mse}")
print(f"[INFO] Mean absolute error is {mae}")

"""ПРЕДСКАЗАНИЕ"""

x = np.array(x_norm)
predicted_y = model.predict(x)
predicted_y

"""ПЕРЕВОДИМ В ВЕКТОРЫ ДЛЯ ПОДСЧЕТА КОРРЕЛЯЦИИ"""

predicted_y = np.reshape(predicted_y, (4209))
y = np.reshape(y, (4209))

"""ПОДСЧЕТ КОРРЕЛЯЦИИ

если коэффициент = 1 или =-1 то зависимость сильная - так должно быть

если коэффициент примерно 0, то зависимость слабая - плохо
"""

kc = np.corrcoef(predicted_y, y)

print(kc)