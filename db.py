import sqlite3

class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect("farmer.db")
        self.cursor = self.conn.cursor()
        self.create_tables()
        print("Database connected: farmer.db")

    def create_tables(self):
        # 1. TABLE FOR FARMERS / USERS (For your App Login)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS farmers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 2. TABLE FOR SENSOR DATA (From ESP32) - CHECKED ✅
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temperature REAL,
                humidity REAL,
                soil INTEGER,
                lux REAL,
                device_id TEXT DEFAULT 'ESP32_01',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 3. TABLE FOR DEVICES - FIXED ✅
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT UNIQUE NOT NULL,
                farmer_phone TEXT,
                is_active INTEGER DEFAULT 1,
                FOREIGN KEY (farmer_phone) REFERENCES farmers (phone)
            )
        """)

        self.conn.commit()
        print("Tables created: farmers, sensor_data, devices")

    # --- Helper functions you will need later ---
    
    def farmer_data(self, name, phone, email, password):
        self.cursor.execute("""
            INSERT INTO farmers (name, phone, email, password) VALUES (?,?,?,?)
        """, (name, phone, email, password))
        self.conn.commit()

    def save_sensor_data(self, temperature, humidity, soil, lux, device_id="ESP32_01"):
        self.cursor.execute("""
            INSERT INTO sensor_data (temperature, humidity, soil, lux, device_id)
            VALUES (?, ?, ?, ?, ?)
        """, (temperature, humidity, soil, lux, device_id))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_latest_data(self):
        self.cursor.execute("""
            SELECT temperature, humidity, soil, lux, created_at
            FROM sensor_data
            ORDER BY id DESC LIMIT 1
        """)
        return self.cursor.fetchone()

    def get_history(self, limit=100):
        self.cursor.execute("""
            SELECT temperature, humidity, soil, lux, created_at
            FROM sensor_data
            ORDER BY id DESC LIMIT ?
        """, (limit,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

# Test it right now - run: python database.py
