import cv2
import face_recognition
import numpy as np
import os
import serial
import time

# --- Serial Setup (Adjust COM port as per your system) ---
try:
    arduino = serial.Serial('COM3', 9600, timeout=1)  # Use '/dev/ttyUSB0' for Linux
    time.sleep(2)  # Wait for Arduino to initialize
    print("Serial connection established.")
except Exception as e:
    arduino = None
    print(f"Serial connection failed: {e}")

# File paths
HOST_IMAGE_PATH = "host_face.jpg"
ENCODINGS_FILE = "host_encoding.npy"

def capture_host_face():
    """Captures and saves the host's face image."""
    cap = cv2.VideoCapture(0)
    print("Capturing host face. Please center your face in the frame.")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        cv2.imshow("Capture Host Face - Press 's' to Save", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            cv2.imwrite(HOST_IMAGE_PATH, frame)
            print("Host face saved!")
            break

    cap.release()
    cv2.destroyAllWindows()
    encode_host_face()

def encode_host_face():
    """Encodes the host's face and saves it."""
    image = face_recognition.load_image_file(HOST_IMAGE_PATH)
    face_encodings = face_recognition.face_encodings(image)

    if face_encodings:
        np.save(ENCODINGS_FILE, face_encodings[0])
        print("Host face encoding saved!")
    else:
        print("No face detected. Try again.")

def load_host_encoding():
    """Loads the host face encoding from file."""
    if os.path.exists(ENCODINGS_FILE):
        return np.load(ENCODINGS_FILE)
    return None

def recognize_face():
    """Recognizes faces in real-time and communicates with Arduino."""
    host_encoding = load_host_encoding()
    if host_encoding is None:
        print("No host encoding found. Capture the host face first.")
        return

    cap = cv2.VideoCapture(0)
    print("Starting real-time recognition. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            match = face_recognition.compare_faces([host_encoding], face_encoding)[0]
            top, right, bottom, left = [v * 4 for v in face_location]

            label = "Host" if match else "Intruder"
            color = (0, 255, 0) if match else (0, 0, 255)

            # Send signal to Arduino
            if arduino:
                try:
                    arduino.write(b'1' if match else b'0')
                    time.sleep(0.1)
                except:
                    pass

            # Draw box and label
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        cv2.imshow("Home Security System", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# --- Main Execution ---
if __name__ == "__main__":
    if not os.path.exists(ENCODINGS_FILE):
        capture_host_face()
    recognize_face()
