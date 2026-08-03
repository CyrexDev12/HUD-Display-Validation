import cv2

cap = cv2.VideoCapture("test/M2/M2Test.mp4")

frame_num = 500

## Set it to that specific frame before reading 
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)

ret, frame = cap.read()

if ret:
    filename = f"frame_{frame_num}.png"
    cv2.imwrite(filename, frame)
    print(f"Saved {filename}")
else:
    print("Failed to capture frame")

cap.release()