import mysql.connector
from mysql.connector import Error

def fetch_data_from_database(query, params=None, commit=False):
    user = 'root'
    password = '20101989'
    host = 'localhost'
    database = 'diplom'
    try:
        # Подключение к базе данных
        cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
        if cnx.is_connected():
            # Создание курсора для выполнения запросов
            cursor = cnx.cursor()
            cursor.execute(query, params)  # Выполнение переданного запроса с параметрами
            if commit:
                cnx.commit()  # Сохранение изменений в базе данных
            # Получение всех результатов запроса
            results = cursor.fetchall()
            return results

    except Error as e:
        print(f"Ошибка: {e}")
        return None

    finally:
        # Закрытие курсора и соединения
        if cnx.is_connected():
            cursor.close()
            cnx.close()


# Пример запроса
# query = 'SELECT username FROM users'
# # Получение данных и преобразование в список имен
# data = fetch_data_from_database(query)
# # Преобразование результата в список имен
# if data is not None:
#     lst = [row[0] for row in data]  # row[0] - это имя пользователя из результата
#     print(lst)
# else:
#     print("Не удалось получить данные.")
