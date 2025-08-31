import cv2
import mediapipe as mp
import time

# Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# For recording
recording = False
video_writer = None

# For trajectory (air V detection)
trajectory = []

def detect_v_shape(traj):
    if len(traj) < 10:
        return False
    mid = len(traj) // 2
    first_half = traj[:mid]
    second_half = traj[mid:]

    dx1 = first_half[-1][0] - first_half[0][0]
    dy1 = first_half[-1][1] - first_half[0][1]
    dx2 = second_half[-1][0] - second_half[0][0]
    dy2 = second_half[-1][1] - second_half[0][1]

    # Rough check for V movement
    if dy1 > 20 and dx1 < -10 and dy2 > 20 and dx2 > 10:
        return True
    return False


while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    h, w, _ = frame.shape

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get landmarks
            landmarks = hand_landmarks.landmark
            index_tip = landmarks[8]
            cx, cy = int(index_tip.x * w), int(index_tip.y * h)

            # Track index finger trajectory for V gesture
            trajectory.append((cx, cy))
            if len(trajectory) > 20:
                trajectory.pop(0)

            if detect_v_shape(trajectory):
                if not recording:
                    fourcc = cv2.VideoWriter_fourcc(*"XVID")
                    filename = f"v_draw_record_{int(time.time())}.avi"
                    video_writer = cv2.VideoWriter(filename, fourcc, 20.0, (w, h))
                    recording = True
                    print("[GESTURE] V drawn in air → Started Recording")
                trajectory.clear()

            # Gesture rules
            finger_tips = [8, 12, 16, 20]
            open_fingers = sum([1 for tip in finger_tips if landmarks[tip].y < landmarks[tip - 2].y])

            thumb_down = landmarks[4].y > landmarks[3].y and landmarks[4].y > landmarks[2].y
            fist = open_fingers == 0
            palm = open_fingers == 4

            if thumb_down:
                print("[GESTURE] Thumb Down → Exiting Camera")
                cap.release()
                if video_writer:
                    video_writer.release()
                cv2.destroyAllWindows()
                exit()

            if fist:
                filename = f"fist_capture_{int(time.time())}.jpg"
                cv2.imwrite(filename, frame)
                print(f"[GESTURE] Fist → Captured {filename}")
                time.sleep(1)  # prevent multiple fast captures

            if palm and recording:
                recording = False
                if video_writer:
                    video_writer.release()
                    video_writer = None
                print("[GESTURE] Palm → Stopped Recording")

    # Write frame if recording
    if recording and video_writer:
        video_writer.write(frame)

    cv2.imshow("Gesture Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
if video_writer:
    video_writer.release()
cv2.destroyAllWindows()
