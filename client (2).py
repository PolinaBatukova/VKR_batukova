import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from sqlquery import *

def submit():
    username = entry_username.get()
    password = entry_password.get()

    # Сравнение введённых данных
    if valid_name(username) and valid_password(password) and valid_isactive(username):
        messagebox.showinfo("Успех", "Вход выполнен успешно!")
        show_buttons()  # Показать дополнительные кнопки после успешного входа
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль.")

def show_buttons():
    # Скрыть поля ввода и кнопку входа
    label_username.pack_forget()
    entry_username.pack_forget()
    label_password.pack_forget()
    entry_password.pack_forget()
    button_submit.pack_forget()

    # Создание дополнительных кнопок
    button_1 = tk.Button(root, text="Показать все заказы", command=show_all_orders)
    button_1.pack(pady=10)

    button_2 = tk.Button(root, text="Заказы в ожидании", command=show_all_expectation_orders)
    button_2.pack(pady=10)

    button_3 = tk.Button(root, text="Заказы в процессе доставки", command=show_all_in_progress_orders)
    button_3.pack(pady=10)

    button_4 = tk.Button(root, text="Выполненные заказы", command=show_all_completed_orders)
    button_4.pack(pady=10)

    button_5 = tk.Button(root, text="Показать всех клиентов", command=show_all_customers)
    button_5.pack(pady=10)

    button_6 = tk.Button(root, text="Показать всех сотрудников", command=show_all_employees)
    button_6.pack(pady=10)

    button_7 = tk.Button(root, text="Обновить статус заказа", command=update_order_status)
    button_7.pack(pady=10)

    button_8 = tk.Button(root, text="Создать заказ", command=create_order)
    button_8.pack(pady=10)

    # Создание виджета Treeview для отображения результатов
    global tree
    tree = ttk.Treeview(root, columns=("order_id", "order_date", "status", "address", "customer_id", "employee_id"), show="headings")
    tree.heading("order_id", text="ID заказа")
    tree.heading("order_date", text="Дата заказа")
    tree.heading("status", text="Статус")
    tree.heading("address", text="Адрес")
    tree.heading("customer_id", text="ID клиента")
    tree.heading("employee_id", text="ID сотрудника")
    tree.pack(pady=10, fill=tk.BOTH, expand=True)

def show_all_orders():
    query = 'SELECT * FROM orders'
    update_treeview(query)

def show_all_expectation_orders():
    query = "SELECT * FROM orders WHERE LOWER(status) = 'в ожидании'"
    update_treeview(query)

def show_all_in_progress_orders():
    query = "SELECT * FROM orders WHERE LOWER(status) = 'в процессе'"
    update_treeview(query)

def show_all_completed_orders():
    query = "SELECT * FROM orders WHERE LOWER(status) = 'доставлено'"
    update_treeview(query)

def show_all_customers():
    query = 'SELECT * FROM clients'
    update_treeview(query, columns=("customer_id", "name", "contact_info"))

def show_all_employees():
    query = 'SELECT * FROM delivery_employees'
    update_treeview(query, columns=("employee_id", "name", "contact_info", "telegramid"))

def update_order_status():
    order_id = simpledialog.askinteger("Введите ID заказа", "ID заказа:")
    if order_id:
        status_window = tk.Toplevel(root)
        status_window.title("Выберите статус")

        def set_status(status):
            query = f"UPDATE orders SET status = '{status}' WHERE order_id = {order_id}"
            fetch_data_from_database(query, commit=True)
            messagebox.showinfo("Успех", "Статус заказа обновлен!")
            show_all_orders()  # Обновить отображение заказов
            status_window.destroy()

        tk.Button(status_window, text="Доставлено", command=lambda: set_status("Доставлено")).pack(pady=10)
        tk.Button(status_window, text="В процессе", command=lambda: set_status("В процессе")).pack(pady=10)
        tk.Button(status_window, text="В ожидании", command=lambda: set_status("В ожидании")).pack(pady=10)
    else:
        messagebox.showerror("Ошибка", "Неверные данные.")

def create_order():
    customer_id = simpledialog.askinteger("Введите ID клиента", "ID клиента:")
    if customer_id:
        address = simpledialog.askstring("Введите адрес", "Адрес:")
        if address:
            employee_id = simpledialog.askinteger("Введите ID сотрудника", "ID сотрудника:")
            if employee_id:
                query = f"INSERT INTO orders (order_date, status, address, customer_id, employee_id) VALUES (NOW(), 'В ожидании', '{address}', {customer_id}, {employee_id})"
                fetch_data_from_database(query, commit=True)
                messagebox.showinfo("Успех", "Заказ создан!")
                show_all_orders()  # Обновить отображение заказов
            else:
                messagebox.showerror("Ошибка", "Неверный ID сотрудника.")
        else:
            messagebox.showerror("Ошибка", "Неверный адрес.")
    else:
        messagebox.showerror("Ошибка", "Неверный ID клиента.")

def update_treeview(query, columns=None):
    if columns:
        tree.configure(columns=columns)
        for col in columns:
            tree.heading(col, text=col.capitalize())
    data = fetch_data_from_database(query)
    if data:
        for row in tree.get_children():
            tree.delete(row)  # Очистка предыдущего содержимого
        for row in data:
            tree.insert("", "end", values=row)
    else:
        messagebox.showerror("Ошибка", "Не удалось выполнить запрос.")

# Создание основного окна
root = tk.Tk()
root.title("Вход в систему")

# Разворачивание окна на весь экран
root.state('zoomed')  # Для Windows
# root.attributes('-fullscreen', True)  # Для других операционных систем

# Создание меток и полей ввода
label_username = tk.Label(root, text="Логин:")
label_username.pack(pady=5)

entry_username = tk.Entry(root)
entry_username.pack(pady=5)

label_password = tk.Label(root, text="Пароль:")
label_password.pack(pady=5)

entry_password = tk.Entry(root, show="*")  # show="*" скрывает вводимый текст
entry_password.pack(pady=5)

# Кнопка для отправки данных
button_submit = tk.Button(root, text="Войти", command=submit)
button_submit.pack(pady=20)

# Запуск главного цикла
root.mainloop()
