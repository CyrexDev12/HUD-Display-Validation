## M2 - ANaylze Every N Frames

import cv2

cap = cv2.VideoCapture("test/M2/M2Test.mp4")

frame_num = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break
        ## Analyzes every 30 frames
    if frame_num % 30 == 0:
        print(f"Analyzing frame {frame_num}")

    frame_num += 1

cap.release()