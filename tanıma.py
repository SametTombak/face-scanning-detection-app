import face_recognition
import cv2
import sqlite3
import numpy as np

# Veritabanından yüz verilerini okuma
def load_faces():
    conn = sqlite3.connect('faces.db')
    c = conn.cursor()
    c.execute("SELECT name, role, image_path FROM faces")
    faces = c.fetchall()
    conn.close()
    return faces

# Yüz verilerini yükleme
known_faces = []
known_names = []
known_role = []

faces = load_faces()

for face in faces:
    name, role, image_path = face
    image = face_recognition.load_image_file(image_path)
    try:
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(f"{name}")
        known_role.append(f"{role}")
    except IndexError:
        print(f"Warning: No face found in {image_path}")

# Kamera başlatma
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Kameradan görüntü alınamıyor.")
        break


    face_locations = face_recognition.face_locations(frame)
    try:
        face_encodings = face_recognition.face_encodings(frame, face_locations)
    except Exception as e:
        print(f"Face encoding error: {e}")
        continue

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.6)
        name = "Tanimsiz"

        face_distances = face_recognition.face_distance(known_faces, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_names[best_match_index]
            role = known_role[best_match_index]

        # Kare içerisine alma ve isim yazma
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        cv2.putText(frame, role, (left + 6, bottom + 30), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
