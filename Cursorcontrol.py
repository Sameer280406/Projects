import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Screen resolution
w_screen, h_screen = pyautogui.size()

cap = cv2.VideoCapture(0)

# States
drag_active = False
scroll_active = False
tap_last_time = 0

# Scroll vars
prev_scroll_y = None
prev_scroll_time = None
SCROLL_SENSITIVITY = 250      # higher = faster scroll
MAX_SCROLL_PER_FRAME = 5

# Tap settings
TAP_DIST = 0.05
TAP_COOLDOWN = 0.25  # seconds

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            lm = hand.landmark

            # fingertip coords
            idx = lm[8]   # index tip
            mid = lm[12]  # middle tip
            thumb = lm[4] # thumb tip

            h, w, _ = frame.shape
            x, y = int(idx.x * w), int(idx.y * h)

            # map to screen instantly (no smoothing for gaming feel)
            screen_x, screen_y = int(idx.x * w_screen), int(idx.y * h_screen)
            pyautogui.moveTo(screen_x, screen_y)

            # Draw cursor point
            cv2.circle(frame, (x, y), 8, (255, 0, 255), cv2.FILLED)

            # ================= Tap (quick index-thumb touch) =================
            idx_thumb_dist = np.linalg.norm([idx.x - thumb.x, idx.y - thumb.y])
            now = time.time()
            if idx_thumb_dist < TAP_DIST and (now - tap_last_time) > TAP_COOLDOWN:
                pyautogui.click()
                tap_last_time = now
                cv2.putText(frame, "Tap!", (x, y - 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # ================= Drag (pinch index + thumb) =================
            if idx_thumb_dist < 0.035:
                if not drag_active:
                    pyautogui.mouseDown()
                    drag_active = True
                    cv2.putText(frame, "Dragging...", (x, y - 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 255), 2)
            else:
                if drag_active:
                    pyautogui.mouseUp()
                    drag_active = False

            # ================= Scroll (index + middle close together) =================
            idx_mid_dist = np.linalg.norm([idx.x - mid.x, idx.y - mid.y])

            if idx_mid_dist < 0.06 and not drag_active:  # fingers close = activate scroll
                scroll_active = True
                avg_y = (idx.y + mid.y) / 2

                if prev_scroll_y is not None and prev_scroll_time is not None:
                    dt = now - prev_scroll_time
                    if dt > 0:
                        dy = prev_scroll_y - avg_y
                        dy_speed = dy / dt  # velocity
                        scroll_amount = int(dy_speed * SCROLL_SENSITIVITY)

                        # clamp
                        scroll_amount = max(-MAX_SCROLL_PER_FRAME,
                                            min(MAX_SCROLL_PER_FRAME, scroll_amount))

                        if scroll_amount != 0:
                            pyautogui.scroll(scroll_amount)
                            cv2.putText(frame, f"Scroll {scroll_amount}", (12, 70),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

                prev_scroll_y = avg_y
                prev_scroll_time = now
            else:
                scroll_active = False
                prev_scroll_y = None
                prev_scroll_time = None

            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Gaming Mouse Hand Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
