from ctypes.wintypes import BOOLEAN
from mysqlconnect import fetch_data_from_database

def valid_name(name):
    query = 'SELECT username FROM users'
    data = fetch_data_from_database(query)
    if data is not None:
        lst = [row[0] for row in data]
        return name in lst
    return False

def valid_password(password):
    query = 'SELECT password_hash FROM users'
    data = fetch_data_from_database(query)
    if data is not None:
        lst = [row[0] for row in data]
        return password in lst
    return False

def valid_isactive(name: str):
    query = 'SELECT is_active FROM users WHERE username = %s'
    params = (name,)
    data = fetch_data_from_database(query, params)
    if data is not None:
        lst = [row[0] for row in data]
        return bool(lst and lst[0])
    return False

def all_orders():
    query = 'SELECT * FROM orders'
    data = fetch_data_from_database(query)
    if data is not None:
        return [row for row in data]
    return []

def check_employees(telegram_id):
    query = 'SELECT name FROM delivery_employees WHERE telegramid = %s'
    params = (telegram_id,)
    data = fetch_data_from_database(query, params)
    if data is not None:
        lst = [row[0] for row in data]
        return len(lst) > 0
    return False

def update_status_order(order_id, status):
    query = 'UPDATE orders SET status = %s WHERE order_id = %s'
    params = (status, order_id)
    fetch_data_from_database(query, params, commit=True)




# print(valid_name(name))
# print(valid_password(password))
# print(valid_isactive(name))
# print(all_orders())
# print(check_employees(1220470635))
# update_status_order(1, 'Доставлено')