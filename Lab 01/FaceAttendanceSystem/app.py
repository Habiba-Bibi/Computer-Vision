import cv2
import sqlite3
from datetime import datetime

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date TEXT,
    time TEXT
)
""")
conn.commit()

cap = cv2.VideoCapture(0)
student_name = "Habiba Bibi"

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

        cursor.execute("SELECT * FROM attendance WHERE name=? AND date=?",
                       (student_name,date))
        record = cursor.fetchone()

        if record is None:
            cursor.execute("INSERT INTO attendance(name,date,time) VALUES(?,?,?)",
                           (student_name,date,time))
            conn.commit()

        cv2.putText(frame,"Attendance Recorded",(x,y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

    cv2.imshow("Face Attendance System",frame)

    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()
conn.close()