## Milestone 2 - Frame by Frame Video Display
import cv2

cap = cv2.VideoCapture("test/M2/M2Test.mp4")

while True:
    ret, frame = cap.read()

    if not ret:
        print("End of video")
        break

    cv2.imshow("Display Recording", frame)

    if cv2.waitKey(30) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()