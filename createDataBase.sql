USE diplom;

CREATE TABLE clients (
    client_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_info TEXT NOT NULL,
    address TEXT
);

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    weight INT CHECK (weight >= 0),
    dimensions VARCHAR(100), -- Габариты можно хранить в формате "Длина x Ширина x Высота"
    stock_quantity INT CHECK (stock_quantity >= 0)
);

CREATE TABLE delivery_employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_info TEXT NOT NULL
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    creation_date DATETIME NOT NULL,
    status VARCHAR(50) NOT NULL,
    delivery_address TEXT NOT NULL,
    orders_client_id INT NOT NULL,
    orders_delivery_employees INT NOT NULL,
    FOREIGN KEY (orders_client_id) REFERENCES clients(client_id),
    FOREIGN KEY (orders_delivery_employees) REFERENCES delivery_employees(employee_id)
);

CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT CHECK (quantity > 0),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
