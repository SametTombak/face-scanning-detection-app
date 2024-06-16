from flask import Flask, request, jsonify, render_template, send_from_directory
import sqlite3
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'

def init_db():
    with sqlite3.connect('faces.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS faces
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     role TEXT NOT NULL,
                     image_path TEXT NOT NULL);''')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/faces', methods=['GET'])
def list_faces():
    conn = sqlite3.connect('faces.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM faces")
    faces = cursor.fetchall()
    conn.close()
    face_list = [{"id": face[0], "name": face[1], "role": face[2], "image_path": face[3]} for face in faces]
    return jsonify(face_list)

@app.route('/get_face/<int:id>', methods=['GET'])
def get_face(id):
    conn = sqlite3.connect('faces.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM faces WHERE id=?", (id,))
    face = cursor.fetchone()
    conn.close()
    if face:
        face_dict = {"id": face[0], "name": face[1], "role": face[2], "image_path": face[3]}
        return jsonify(face_dict)
    return jsonify({"error": "face not found"}), 404

@app.route('/add_face', methods=['POST'])
def add_face():
    name = request.form['name']
    role = request.form['role']
    photo = request.files['photo']
    photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
    photo.save(photo_path)
    conn = sqlite3.connect('faces.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO faces (name, role, image_path) VALUES (?, ?, ?)", (name, role, photo.filename))
    conn.commit()
    conn.close()
    return '', 201

@app.route('/update_face/<int:id>', methods=['POST'])
def update_face(id):
    name = request.form['name']
    role = request.form['role']
    photo = request.files.get('photo')
    conn = sqlite3.connect('faces.db')
    cursor = conn.cursor()
    if photo:
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
        photo.save(photo_path)
        cursor.execute("UPDATE faces SET name=?, role=?, image_path=? WHERE id=?", (name, role, photo.filename, id))
    else:
        cursor.execute("UPDATE faces SET name=?, role=? WHERE id=?", (name, role, id))
    conn.commit()
    conn.close()
    return '', 204

@app.route('/delete_face/<int:id>', methods=['DELETE'])
def delete_face(id):
    conn = sqlite3.connect('faces.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM faces WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return '', 204

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
