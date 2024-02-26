import sqlite3

def init_db():
    conn = sqlite3.connect(r'C:\Users\osandal\Downloads\Tinker Project\Burger-Shop\customer.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
