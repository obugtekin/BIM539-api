import sqlite3

DB_PATH = 'database.sqlite'
TEST_DB_PATH = None

def get_db(db_path=None):
    if db_path is None:
        if TEST_DB_PATH is not None:
            db_path = TEST_DB_PATH
        else:
            db_path = DB_PATH
    conn = sqlite3.connect(db_path)
    return conn

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            created_at TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            category_id INTEGER,
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            order_date TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT,
            created_at TEXT
        )
    ''')
    
    cursor.execute('SELECT COUNT(*) as count FROM users')
    if cursor.fetchone()[0] == 0:
        print('Örnek veriler ekleniyor...')
        
        cursor.execute("INSERT INTO categories (name, description) VALUES (?, ?)", 
                      ('Elektronik', 'Elektronik ürünler'))
        cursor.execute("INSERT INTO categories (name, description) VALUES (?, ?)", 
                      ('Giyim', 'Giyim ve aksesuar ürünleri'))
        
        cursor.execute("INSERT INTO users (name, email, phone) VALUES (?, ?, ?)", 
                      ('ONUR BUĞTEKİN', 'onur@example.com', '555-0101'))
        cursor.execute("INSERT INTO users (name, email, phone) VALUES (?, ?, ?)", 
                      ('ONUR BUĞTEKİN', 'onur2@example.com', '555-0102'))
        
        cursor.execute("INSERT INTO products (name, description, price, stock, category_id) VALUES (?, ?, ?, ?, ?)", 
                      ('Laptop', 'Yüksek performanslı laptop', 15000.00, 10, 1))
        cursor.execute("INSERT INTO products (name, description, price, stock, category_id) VALUES (?, ?, ?, ?, ?)", 
                      ('Tişört', 'Rahat pamuklu tişört', 150.00, 50, 2))
        
        print('Örnek veriler eklendi.')
    
    conn.commit()
    conn.close()
    print('Veritabanı hazır.')
