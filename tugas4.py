import cv2
import mediapipe as mp
import pygame

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
# finger_images = [cv2.imread(f"./jari/{i}.jpg") for i in range(1, 11)]

# for i in range(10):
#     finger_images[i] = cv2.resize(finger_images[i], (100, 100))

pygame.mixer.init()
sound = pygame.mixer.Sound('blowsup.wav')

i = 0
while cap.isOpened():
    success, img = cap.read()
    if not success:
        continue

    img = cv2.flip(img, 1)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_img)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            finger_landmarks = hand_landmarks.landmark
            

            right_finger_tips = [20, 16, 12, 8, 4]
            right_knuckles = [18, 14, 10, 6, 2]

            left_finger_tips = [4, 8, 12, 16, 20]
            left_knuckles = [2, 6, 10, 14, 18]
            

            right_fingers_up = sum(1 for tip, knuckle in zip(right_finger_tips, right_knuckles) if finger_landmarks[tip].y < finger_landmarks[knuckle].y)
            left_fingers_up = sum(1 for tip, knuckle in zip(left_finger_tips, left_knuckles) if finger_landmarks[tip].y < finger_landmarks[knuckle].y)
            
            total_fingers_up = left_fingers_up + right_fingers_up
            fingers_down = 10 - total_fingers_up

            print(f"Fingers Up: {total_fingers_up}, Fingers Down: {fingers_down}")
            if total_fingers_up > 0 and total_fingers_up <= 10:
                # cv2.imshow("Finger Image", finger_images[total_fingers_up - 1])
                if i != fingers_down:
                    i=fingers_down
                    sound.play()

    cv2.imshow("hitung jari", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()