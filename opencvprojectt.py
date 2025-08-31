import cv2
import mediapipe as mp
import numpy as np
import time
import math
from collections import deque

# Mediapipe setup
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Eye landmark indices
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# Helper functions
def euclidean(pt1, pt2):
    return math.dist(pt1, pt2)

def eye_aspect_ratio(eye_landmarks):
    vert1 = euclidean(eye_landmarks[1], eye_landmarks[5])
    vert2 = euclidean(eye_landmarks[2], eye_landmarks[4])
    hor = euclidean(eye_landmarks[0], eye_landmarks[3])
    return (vert1 + vert2) / (2.0 * hor)

# EAR Threshold
EAR_THRESHOLD = 0.25
BLINK_CONSEC_FRAMES = 3  # Require at least 3 frames of closure
blink_counter = 0
photo_counter = 0
video_writer = None
recording = False

# Debounce timers
last_photo_time = 0
last_blink_time = 0
PHOTO_COOLDOWN = 1.5  # seconds
BLINK_COOLDOWN = 1.5  # seconds

# EAR smoothing
ear_history = deque(maxlen=5)

cap = cv2.VideoCapture(0)

print("👉 Controls: Blink OR Fist = Photo | V-sign = Start Video | Palm = Stop Video | Thumbs Down = Exit")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_results = face_mesh.process(rgb_frame)
    hand_results = hands.process(rgb_frame)

    # Eye blink detection
    if face_results.multi_face_landmarks:
        for face_landmarks in face_results.multi_face_landmarks:
            left_eye = [(int(face_landmarks.landmark[i].x * w), int(face_landmarks.landmark[i].y * h)) for i in LEFT_EYE]
            right_eye = [(int(face_landmarks.landmark[i].x * w), int(face_landmarks.landmark[i].y * h)) for i in RIGHT_EYE]

            left_ear = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)
            ear = (left_ear + right_ear) / 2.0

            ear_history.append(ear)
            smoothed_ear = sum(ear_history) / len(ear_history)

            eye_color = (0, 255, 0) if smoothed_ear > EAR_THRESHOLD else (0, 0, 255)
            cv2.polylines(frame, [np.array(left_eye)], True, eye_color, 2)
            cv2.polylines(frame, [np.array(right_eye)], True, eye_color, 2)

            if smoothed_ear < EAR_THRESHOLD:
                blink_counter += 1
            else:
                if blink_counter >= BLINK_CONSEC_FRAMES and (time.time() - last_blink_time) > BLINK_COOLDOWN:
                    photo_counter += 1
                    filename = f"blink_photo_{photo_counter}.jpg"
                    cv2.imwrite(filename, frame)
                    last_blink_time = time.time()
                    print(f"📸 Blink detected → Saved {filename}")
                blink_counter = 0

    # Hand gesture detection
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks.landmark]

            now = time.time()

            # Thumbs down → Exit
            if landmarks[4][1] > landmarks[3][1] and landmarks[4][1] > landmarks[5][1]:
                print("👎 Exiting...")
                cap.release()
                cv2.destroyAllWindows()
                exit()

            # Open palm = Stop recording
            fingers_open = [landmarks[8][1] < landmarks[6][1],
                            landmarks[12][1] < landmarks[10][1],
                            landmarks[16][1] < landmarks[14][1],
                            landmarks[20][1] < landmarks[18][1]]
            if all(fingers_open):
                if recording:
                    print("🛑 Palm → Stop recording")
                    recording = False
                    video_writer.release()
                    video_writer = None

            # Closed fist = Take photo
            if all([landmarks[8][1] > landmarks[6][1],
                    landmarks[12][1] > landmarks[10][1],
                    landmarks[16][1] > landmarks[14][1],
                    landmarks[20][1] > landmarks[18][1]]):
                if (now - last_photo_time) > PHOTO_COOLDOWN:
                    photo_counter += 1
                    filename = f"fist_photo_{photo_counter}.jpg"
                    cv2.imwrite(filename, frame)
                    last_photo_time = now
                    print(f"✊ Fist detected → Saved {filename}")

            # V-sign = Start recording
            if (landmarks[8][1] < landmarks[6][1] and
                landmarks[12][1] < landmarks[10][1] and
                landmarks[16][1] > landmarks[14][1] and
                landmarks[20][1] > landmarks[18][1]):
                if not recording:
                    print("🎥 V-sign → Start recording")
                    recording = True
                    video_filename = f"video_{int(time.time())}.avi"
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    video_writer = cv2.VideoWriter(video_filename, fourcc, 20.0, (w, h))

    # Save video frames
    if recording and video_writer:
        video_writer.write(frame)
        cv2.putText(frame, "REC", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

    cv2.imshow("Eye & Hand Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
if video_writer:
    video_writer.release()
cv2.destroyAllWindows()
