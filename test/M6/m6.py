# Milestone 6 - Video Frame Comparison
# Enhanced SSIM Analysis

import cv2
import statistics
from skimage.metrics import structural_similarity as ssim

# -------------------------
# Settings
# -------------------------

VIDEO_PATH = "test/M6/M6_Test1.mp4"
GOLDEN_IMAGE_PATH = "test/M6/Golden.png"

FRAME_INTERVAL = 20
SIMILARITY_THRESHOLD = 0.983

# -------------------------
# Load Golden Image
# -------------------------

golden = cv2.imread(GOLDEN_IMAGE_PATH)

if golden is None:
    raise FileNotFoundError(
        f"Could not load {GOLDEN_IMAGE_PATH}"
    )

golden_gray = cv2.cvtColor(
    golden,
    cv2.COLOR_BGR2GRAY
)

# -------------------------
# Open Video
# -------------------------

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    raise Exception(
        f"Could not open {VIDEO_PATH}"
    )

# -------------------------
# Statistics
# -------------------------

frame_number = 0

frames_checked = 0
fail_count = 0

ssim_scores = []

# -------------------------
# Analysis
# -------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        break

    if frame_number % FRAME_INTERVAL == 0:

        current_gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        if current_gray.shape != golden_gray.shape:

            print(
                f"Frame {frame_number}: "
                f"FAIL (size mismatch)"
            )

            frame_number += 1
            continue

        score, _ = ssim(
            golden_gray,
            current_gray,
            full=True
        )

        ssim_scores.append(score)

        frames_checked += 1

        if score >= SIMILARITY_THRESHOLD:

            result = "PASS"

        else:

            result = "FAIL"
            fail_count += 1

        print(
            f"Frame {frame_number:5d}: "
            f"{result} "
            f"(SSIM = {score:.6f})"
        )

    frame_number += 1

cap.release()

# -------------------------
# Summary
# -------------------------

print()
print("=" * 60)
print("SUMMARY")
print("=" * 60)

print(f"Frames Checked:      {frames_checked}")
print(f"Failed Frames:       {fail_count}")

if frames_checked > 0:

    fail_rate = (
        fail_count / frames_checked
    ) * 100

    avg_ssim = statistics.mean(
        ssim_scores
    )

    min_ssim = min(
        ssim_scores
    )

    max_ssim = max(
        ssim_scores
    )

    std_dev = statistics.stdev(
        ssim_scores
    ) if len(ssim_scores) > 1 else 0

    print(
        f"Average SSIM:        "
        f"{avg_ssim:.6f}"
    )

    print(
        f"Minimum SSIM:        "
        f"{min_ssim:.6f}"
    )

    print(
        f"Maximum SSIM:        "
        f"{max_ssim:.6f}"
    )

    print(
        f"SSIM Std Dev:        "
        f"{std_dev:.6f}"
    )

    print(
        f"Failure Rate:        "
        f"{fail_rate:.2f}%"
    )

    # -------------------------
    # Flicker Assessment
    # -------------------------

    if std_dev > 0.01:
        print(
            "Assessment: "
            "Possible intermittent flicker "
            "(high SSIM variation)"
        )
    else:
        print(
            "Assessment: "
            "Display appears stable"
        )

print("=" * 60)

print("Testing Complete")