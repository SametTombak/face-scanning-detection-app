import sqlite3

# Veritabanı oluşturma
conn = sqlite3.connect('faces.db')
c = conn.cursor()

# Tablo oluşturma
c.execute('''CREATE TABLE IF NOT EXISTS faces
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              role TEXT NOT NULL,
              image_path TEXT NOT NULL)''')

# Veritabanı bağlantısını kapatma
conn.commit()
conn.close()
