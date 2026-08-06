# Milestone 5 - Static and Dynamic Validation all in one
import cv2
import numpy as np
import math
from skimage.metrics import structural_similarity as ssim

# --------------------------------------------------
# Inputs
# --------------------------------------------------

VIDEO_PATH = "test/M5/T3_3Video.mp4"
GOLDEN_IMAGE_PATH = "test/M5/Golden_Img.png"

FRAME_INTERVAL = 20

SIMILARITY_THRESHOLD = 0.90
MIN_CCW_RATIO = 0.80

# --------------------------------------------------
# Load Golden Image
# --------------------------------------------------

golden = cv2.imread(GOLDEN_IMAGE_PATH)

if golden is None:
    raise FileNotFoundError(
        f"Could not load {GOLDEN_IMAGE_PATH}"
    )

golden_gray = cv2.cvtColor(
    golden,
    cv2.COLOR_BGR2GRAY
)

# --------------------------------------------------
# Open Video
# --------------------------------------------------

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    raise Exception(
        f"Could not open {VIDEO_PATH}"
    )

# --------------------------------------------------
# Tracking Variables
# --------------------------------------------------

angles = []

static_passes = 0
static_fails = 0

frame_number = 0

# --------------------------------------------------
# Process Video
# --------------------------------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        break

    if frame_number % FRAME_INTERVAL == 0:

        print(
            f"\n--- Frame {frame_number} ---"
        )

        # ==========================================
        # Static Validation (Milestone 3)
        # ==========================================

        current_gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        if current_gray.shape == golden_gray.shape:

            score, _ = ssim(
                golden_gray,
                current_gray,
                full=True
            )

            if score >= SIMILARITY_THRESHOLD:

                static_passes += 1

                print(
                    f"Static PASS "
                    f"(SSIM={score:.4f})"
                )

            else:

                static_fails += 1

                print(
                    f"Static FAIL "
                    f"(SSIM={score:.4f})"
                )

        else:

            static_fails += 1

            print(
                "Static FAIL "
                "(Size Mismatch)"
            )

        # ==========================================
        # Dynamic Validation (Milestone 4)
        # ==========================================

        height, width = frame.shape[:2]

        center_x = width // 2
        center_y = height // 2

        hsv = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2HSV
        )

        lower_green = np.array(
            [40, 40, 40]
        )

        upper_green = np.array(
            [90, 255, 255]
        )

        mask = cv2.inRange(
            hsv,
            lower_green,
            upper_green
        )

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if len(contours) > 0:

            best_contour = None
            best_distance = 0

            for contour in contours:

                M = cv2.moments(contour)

                if M["m00"] == 0:
                    continue

                cx = int(
                    M["m10"] / M["m00"]
                )

                cy = int(
                    M["m01"] / M["m00"]
                )

                distance = math.sqrt(
                    (cx - center_x) ** 2 +
                    (cy - center_y) ** 2
                )

                if distance > best_distance:

                    best_distance = distance
                    best_contour = contour

            if best_contour is not None:

                M = cv2.moments(
                    best_contour
                )

                if M["m00"] != 0:

                    arrow_x = int(
                        M["m10"] / M["m00"]
                    )

                    arrow_y = int(
                        M["m01"] / M["m00"]
                    )

                    angle = math.degrees(
                        math.atan2(
                            arrow_y - center_y,
                            arrow_x - center_x
                        )
                    )

                    angles.append(angle)

                    print(
                        f"Dynamic Track "
                        f"Angle={angle:.2f}"
                    )

    frame_number += 1

cap.release()

# --------------------------------------------------
# Dynamic Analysis
# --------------------------------------------------

ccw_count = 0
total_moves = 0

print("\n========== ANGLE ANALYSIS ==========")

for i in range(1, len(angles)):

    previous = angles[i - 1]
    current = angles[i]

    delta = current - previous

    if delta > 180:
        delta -= 360

    elif delta < -180:
        delta += 360

    total_moves += 1

    direction = "CW/STATIC"

    if delta < 0:
        ccw_count += 1
        direction = "CCW"

    print(
        f"Step {i}: "
        f"Delta={delta:.2f} "
        f"{direction}"
    )

# --------------------------------------------------
# Results
# --------------------------------------------------

if total_moves > 0:
    ccw_ratio = ccw_count / total_moves
else:
    ccw_ratio = 0

total_static = (
    static_passes + static_fails
)

if total_static > 0:
    static_ratio = (
        static_passes / total_static
    )
else:
    static_ratio = 0

dynamic_pass = (
    ccw_ratio >= MIN_CCW_RATIO
)

static_pass = (
    static_ratio >= 0.80
)

print("\n========== SUMMARY ==========")

print(
    f"Static Passes: "
    f"{static_passes}"
)

print(
    f"Static Fails: "
    f"{static_fails}"
)

print(
    f"Static Pass Ratio: "
    f"{static_ratio:.2%}"
)

print(
    f"CCW Ratio: "
    f"{ccw_ratio:.2%}"
)

print(
    f"Dynamic Result: "
    f"{'PASS' if dynamic_pass else 'FAIL'}"
)

print(
    f"Static Result: "
    f"{'PASS' if static_pass else 'FAIL'}"
)

overall_pass = (
    dynamic_pass and static_pass
)

print(
    f"\nOVERALL RESULT: "
    f"{'PASS' if overall_pass else 'FAIL'}"
)