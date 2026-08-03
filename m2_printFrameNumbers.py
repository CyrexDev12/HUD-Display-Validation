## Milestone 2 - Print Frame Numbers

import cv2

cap = cv2.VideoCapture("test/M2/M2Test.mp4")

frame_num = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    print(f"Processing frame {frame_num}")

    frame_num += 1

cap.release()