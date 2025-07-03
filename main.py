import cv2
import datetime
import os
import winsound  # 🔔 Built-in module for Windows beep

# === Step 1: Load Haar Cascades === #
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# === Step 2: Initialize Webcam === #
cap = cv2.VideoCapture(0)

# === Step 3: Sound Alert Function === #
def play_alert():
    # Frequency = 1000 Hz, Duration = 500 ms
    winsound.Beep(1000, 500)

# === Step 4: Print and Log Violation (no file creation) === #
def log_violation(reason):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"[{timestamp}] Violation: {reason}"
    print(message)
    play_alert()

print("📷 Cheat Detection Started. Press 'q' to exit.\n")

# === Step 5: Monitoring Loop === #
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        log_violation("No face detected")
    elif len(faces) > 1:
        log_violation("Multiple faces detected")
    else:
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            eyes = eye_cascade.detectMultiScale(roi_gray)
            if len(eyes) < 2:
                log_violation("Eyes not properly detected")
            else:
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    cv2.imshow("Exam Monitor", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# === Step 6: Cleanup === #
cap.release()
cv2.destroyAllWindows()
