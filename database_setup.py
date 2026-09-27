import sqlite3
import random

random.seed(42)

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS sales")
cursor.execute("DROP TABLE IF EXISTS customers")
cursor.execute("DROP TABLE IF EXISTS products")

cursor.execute("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    region TEXT
)
""")

cursor.execute("""
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT
)
""")

cursor.execute("""
CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    revenue INTEGER,
    month TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id)
)
""")

regions = ["North", "South", "East", "West"]
customers_data = []

for i in range(1, 8):
    customers_data.append((i, f"Customer_{i}", random.choice(regions)))

cursor.executemany(
    "INSERT INTO customers VALUES (?, ?, ?)",
    customers_data
)

categories = ["Electronics", "Mobile", "Accessories"]
products_data = []

for i in range(1, 6):
    products_data.append((i, f"Product_{i}", random.choice(categories)))

cursor.executemany(
    "INSERT INTO products VALUES (?, ?, ?)",
    products_data
)

months = ["Jan", "Feb", "Mar", "Apr"]
sales_data = []

for i in range(1, 51):
    sales_data.append((
        i,
        random.randint(1, 7),
        random.randint(1, 5),
        random.randint(500, 2000),
        random.choice(months)
    ))

cursor.executemany(
    "INSERT INTO sales VALUES (?, ?, ?, ?, ?)",
    sales_data
)

conn.commit()
conn.close()

print("Multi-table database created successfully!")