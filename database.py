import sqlite3

def init_db():
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercise TEXT NOT NULL,
        duration REAL NOT NULL,
        calories_burned REAL NOT NULL,
        date TEXT NOT NULL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS food (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL,
        calories REAL NOT NULL,
        meal_type TEXT DEFAULT 'Snack',
        date TEXT NOT NULL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS water (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        date TEXT NOT NULL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY,
        calorie_goal REAL DEFAULT 2000,
        burn_goal REAL DEFAULT 500,
        water_goal REAL DEFAULT 2.0,
        workout_minutes_goal REAL DEFAULT 30,
        steps_goal INTEGER DEFAULT 8000,
        weight_goal REAL DEFAULT 0
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS daily_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT UNIQUE NOT NULL,
        weight REAL DEFAULT 0,
        steps INTEGER DEFAULT 0
    )''')

    c.execute('INSERT OR IGNORE INTO goals (id) VALUES (1)')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect('fitness.db')
    conn.row_factory = sqlite3.Row
    return conn
print("databse created")