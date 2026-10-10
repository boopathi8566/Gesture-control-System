import cv2
import mediapipe as mp
import pyautogui
import time
import os
import winsound

# ==========================================
# CAMERA
# ==========================================
cap = cv2.VideoCapture(0)

# ==========================================
# MEDIAPIPE HANDS
# ==========================================
mp_hands = mp.solutions.hands88888

hands = mp_hands.Hands(
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8,
    max_num_hands=1
)

# ==========================================
# DELAY SYSTEM
# ==========================================
last_action_time = 0
delay = 1.5

# ==========================================
# SAVE PATH
# ==========================================
save_path = r"C:\Users\Boopathi vasan\OneDrive\Documents\programs"

# ==========================================
# MAIN LOOP
# ==========================================
while True:

    success, img = cap.read()

    if not success:
        break

    # Mirror Effect
    img = cv2.flip(img, 1)

    h, w, _ = img.shape

    # RGB Conversion
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Hand Detection
    result = hands.process(rgb)

    gesture_text = "Waiting..."

    # ==========================================
    # DETECTION BOX
    # ==========================================
    box_x1 = 150
    box_y1 = 100

    box_x2 = w - 150
    box_y2 = h - 100

    cv2.rectangle(
        img,
        (box_x1, box_y1),
        (box_x2, box_y2),
        (0, 255, 0),
        3
    )

    cv2.putText(
        img,
        "Gesture Area",
        (box_x1, box_y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    # ==========================================
    # HAND LANDMARKS
    # ==========================================
    if result.multi_hand_landmarks:

        for hand_landmarks in result.multi_hand_landmarks:

            lm = []

            for id, landmark in enumerate(hand_landmarks.landmark):

                cx = int(landmark.x * w)
                cy = int(landmark.y * h)

                lm.append((id, cx, cy))

            # Draw Hand Landmarks
            mp.solutions.drawing_utils.draw_landmarks(
                img,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # ==========================================
            # GESTURE LOGIC
            # ==========================================
            if lm:

                # Finger Positions
                x1, y1 = lm[8][1], lm[8][2]
                x2, y2 = lm[4][1], lm[4][2]

                current_time = time.time()

                # ==========================================
                # ONLY INSIDE BOX
                # ==========================================
                if (
                    box_x1 < x1 < box_x2 and
                    box_y1 < y1 < box_y2
                ):
     
                    # =====================================
                    # 🤏 SCREENSHOT (FIXED)
                    # =====================================
                    if (
                        abs(x1 - x2) < 25 and
                        abs(y1 - y2) < 25 and

                        # Index finger slightly open
                        lm[8][2] < lm[7][2] and

                        # Middle folded
                        lm[12][2] > lm[10][2] and

                        # Ring folded
                        lm[16][2] > lm[14][2] and

                        # Pinky folded
                        lm[20][2] > lm[18][2] and

                        current_time - last_action_time > delay
                    ):

                        filename = os.path.join(
                            save_path,
                            f"screenshot_{int(time.time())}.png"
                        )

                        pyautogui.screenshot(filename)

                        gesture_text = "Screenshot Taken"

                        print("Screenshot Taken")

                        winsound.Beep(1000, 200)

                        last_action_time = current_time

                    # =====================================
                    # ✊ OPEN POWERPOINT
                    # =====================================
                    elif (
                        lm[8][2] > lm[5][2] and
                        lm[12][2] > lm[9][2] and
                        lm[16][2] > lm[13][2] and
                        lm[20][2] > lm[17][2] and
                        current_time - last_action_time > delay
                    ):

                        os.startfile("powerpnt.exe")

                        gesture_text = "PowerPoint Opened"

                        print("PowerPoint Opened")

                        winsound.Beep(1300, 200)

                        last_action_time = current_time

                    # =====================================
                    # 🖐️ HOME / DESKTOP
                    # =====================================
                    elif (
                        lm[8][2] < lm[6][2] and
                        lm[12][2] < lm[10][2] and
                        lm[16][2] < lm[14][2] and
                        lm[20][2] < lm[18][2] and
                        current_time - last_action_time > delay
                    ):

                        pyautogui.hotkey('win', 'd')

                        gesture_text = "Desktop Opened"

                        print("Desktop Opened")

                        winsound.Beep(800, 300)

                        last_action_time = current_time

                    # =====================================
                    # ✌️ NEXT SLIDE
                    # =====================================
                    elif (
                        lm[8][2] < lm[6][2] and
                        lm[12][2] < lm[10][2] and
                        lm[16][2] > lm[14][2] and
                        lm[20][2] > lm[18][2] and
                        current_time - last_action_time > delay
                    ):

                        pyautogui.press('right')

                        gesture_text = "Next Slide"

                        print("Next Slide")

                        winsound.Beep(1500, 200)

                        last_action_time = current_time

                    # =====================================
                    # ☝️ PREVIOUS SLIDE
                    # =====================================
                    elif (
                        lm[8][2] < lm[6][2] and
                        lm[12][2] > lm[10][2] and
                        lm[16][2] > lm[14][2] and
                        lm[20][2] > lm[18][2] and
                        current_time - last_action_time > delay
                    ):

                        pyautogui.press('left')

                        gesture_text = "Previous Slide"

                        print("Previous Slide")

                        winsound.Beep(700, 200)

                        last_action_time = current_time

    # ==========================================
    # STATUS BAR
    # ==========================================
    cv2.rectangle(img, (10, 10), (500, 70), (0, 0, 0), -1)

    cv2.putText(
        img,
        gesture_text,
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # ==========================================
    # SHOW WINDOW
    # ==========================================
    cv2.imshow("Gesture Control System", img)

    # ESC TO EXIT
    if cv2.waitKey(1) == 27:
        break

# ==========================================
# RELEASE
# ==========================================
cap.release()
cv2.destroyAllWindows()