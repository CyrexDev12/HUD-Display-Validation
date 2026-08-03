#M# Milestone 3 - Video Frame Comparison
import cv2
from skimage.metrics import structural_similarity as ssim

# Settings
VIDEO_PATH = "test/M3/M3V1.mp4"
GOLDEN_IMAGE_PATH = "test/M3/Golden.png"

FRAME_INTERVAL = 20
SIMILARITY_THRESHOLD = 0.95

# Load golden image
golden = cv2.imread(GOLDEN_IMAGE_PATH)

if golden is None:
    raise FileNotFoundError(
        f"Could not load {GOLDEN_IMAGE_PATH}"
    )

golden_gray = cv2.cvtColor(golden, cv2.COLOR_BGR2GRAY)

# Open video
cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    raise Exception(
        f"Could not open {VIDEO_PATH}"
    )

frame_number = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    if frame_number % FRAME_INTERVAL == 0:

        current_gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        # # Ensure dimensions match
        # if current_gray.shape != golden_gray.shape:
        #     print(
        #         f"Frame {frame_number}: "
        #         f"FAIL (size mismatch)"
        #     )
        #     frame_number += 1
        #     continue

        score, _ = ssim(
            golden_gray,
            current_gray,
            full=True
        )

        if score >= SIMILARITY_THRESHOLD:
            print(
                f"Frame {frame_number}: PASS "
                f"(Score={score:.4f})"
            )
        else:
            print(
                f"Frame {frame_number}: FAIL "
                f"(Score={score:.4f})"
            )

    frame_number += 1

cap.release()

print("Testing Complete")