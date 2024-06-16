import sqlite3

# Yüz verilerini ekleme
def insert_face(name, role, image_path):
    conn = sqlite3.connect('faces.db')
    c = conn.cursor()
    c.execute("INSERT INTO faces (name, role, image_path) VALUES (?, ?, ?)", (name, role, image_path))
    conn.commit()
    conn.close()

# Örnek yüz verileri
insert_face('Samet Tombak', 'Öğrenci', 'samet.jpg')
insert_face('Selim Zengin', 'Öğrenci', 'selim.jpg')
insert_face('Sedat Yilmaz', 'Suçlu', 'sedat.jpg')
insert_face('Metehan Tut', 'Kayip Öğrenci', 'metehan.jpg')
insert_face('Gülcan Canbolat', 'Hoca', 'gulcanhoca.jpg')
