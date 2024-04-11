import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_x, index_y = 0, 0

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, flipCode=1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark

            if len(landmarks) >= 9:
                index_landmark = landmarks[8]
                x = int(index_landmark.x * frame_width)
                y = int(index_landmark.y * frame_height)
                cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                index_x = screen_width / frame_width * x
                index_y = screen_height / frame_height * y

            if len(landmarks) >= 5:
                thumb_landmark = landmarks[4]
                x = int(thumb_landmark.x * frame_width)
                y = int(thumb_landmark.y * frame_height)
                cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                thumb_x = screen_width / frame_width * x
                thumb_y = screen_height / frame_height * y

                if abs(index_y - thumb_y) < 20:
                    pyautogui.click()
                    pyautogui.sleep(0.1)  # Reduced sleep time
                elif abs(index_y - thumb_y) < 100:
                    pyautogui.moveTo(index_x, index_y)

    cv2.imshow('Virtual Mouse', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
