import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = "study_share.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            department TEXT,
            year INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            course TEXT NOT NULL,
            file_url TEXT NOT NULL,
            user_id INTEGER,
            uploaded_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully.")

def create_user(email, password, name, department, year):
    conn = get_connection()
    cursor = conn.cursor()

    password_hash = generate_password_hash(password)

    try:
        cursor.execute("""
            INSERT INTO users (email, password_hash, name, department, year)
            VALUES (?, ?, ?, ?, ?)
        """, (email, password_hash, name, department, year))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    
    conn.close()
    return success

def verify_user(email, password):
    conn = get_connection() 
    cursor = conn.cursor() 

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    conn.close() 

    if user and check_password_hash(user[2], password):
        return user 
    return None 

def add_material(title, course, file_url, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    uploaded_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    cursor.execute("""
        INSERT INTO materials (title, course, file_url, user_id, uploaded_at)
        VALUES (?, ?, ?, ?, ?)
    """, (title, course, file_url, user_id, uploaded_at))

    conn.commit()
    conn.close()
    print(f"Material '{title}' added successfully.")

def get_all_materials():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT materials.id, materials.title, materials.course, 
               materials.file_url, materials.uploaded_at, users.name
        FROM materials
        JOIN users ON materials.user_id = users.id
        ORDER BY materials.uploaded_at DESC
    """)
    materials = cursor.fetchall()

    conn.close()
    return materials    

if __name__ == "__main__":
    create_tables()    
    user = verify_user("test@bdu.edu.et", "password123")
    print("Login successful:", user) if user else print("Login failed")

    user = verify_user("test@bdu.edu.et", "wrongpassword")
    print("Login successful:", user) if user else print("Login failed")