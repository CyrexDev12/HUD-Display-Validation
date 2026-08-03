## Milestone 2 - OpenCV Video Capture Properties
import cv2

video_path = "test/M2/M2Test.mp4"

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    raise Exception(f"Could not open {video_path}")

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

duration = frame_count / fps if fps > 0 else 0

print(f"Resolution : {width}x{height}")
print(f"FPS        : {fps:.2f}")
print(f"Frames     : {frame_count}")
print(f"Duration   : {duration:.2f} seconds")

cap.release()