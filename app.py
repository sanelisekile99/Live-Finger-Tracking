import cv2
import mediapipe as mp
import serial
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Set up serial connection to Arduino (update COM3 to your Arduino port)
arduino = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)  # Wait for Arduino to reset

camera = cv2.VideoCapture(0)

while True:
    success, frame = camera.read()
    if not success:
        continue
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    finger_positions = [0, 0, 0, 0, 0]
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        tip_ids = [mp_hands.HandLandmark.THUMB_TIP,
                   mp_hands.HandLandmark.INDEX_FINGER_TIP,
                   mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                   mp_hands.HandLandmark.RING_FINGER_TIP,
                   mp_hands.HandLandmark.PINKY_TIP]
        for i, tip_id in enumerate(tip_ids):
            x = hand_landmarks.landmark[tip_id].x  # normalized [0,1]
            finger_positions[i] = x
    # Send finger positions to Arduino as comma-separated string
    data_str = ','.join([f'{v:.2f}' for v in finger_positions]) + '\n'
    arduino.write(data_str.encode('utf-8'))
    cv2.imshow('Hand Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()
arduino.close()