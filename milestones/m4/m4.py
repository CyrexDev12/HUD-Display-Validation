## Milestone 4 - Detect Counter Clockwise Rotation
## Tracks Green Navigation Arrow

import cv2
import numpy as np
import math

VIDEO_PATH = "test/M4/nomotion_video.mp4"

FRAME_INTERVAL = 5
MIN_CCW_RATIO = 0.80

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    raise Exception(
        f"Could not open {VIDEO_PATH}"
    )

angles = []
frame_number = 0

while True:

    ret, frame = cap.read()

    if not ret:
        break

    if frame_number % FRAME_INTERVAL == 0:

        height, width = frame.shape[:2]

        center_x = width // 2
        center_y = height // 2

        hsv = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2HSV
        )

        # Green detection range
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

        if len(contours) == 0:

            print(
                f"Frame {frame_number}: "
                f"No green object detected"
            )

            frame_number += 1
            continue

        best_contour = None
        best_distance = 0

        for contour in contours:

            M = cv2.moments(contour)

            if M["m00"] == 0:
                continue

            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            distance = math.sqrt(
                (cx - center_x) ** 2 +
                (cy - center_y) ** 2
            )

            if distance > best_distance:
                best_distance = distance
                best_contour = contour

        green_contour = best_contour

        area = cv2.contourArea(
            green_contour
        )

        M = cv2.moments(
            green_contour
        )

        if M["m00"] == 0:

            print(
                f"Frame {frame_number}: "
                f"Invalid contour"
            )

            frame_number += 1
            continue

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
            f"Frame {frame_number}: "
            f"Arrow=({arrow_x},{arrow_y}) "
            f"Area={area:.1f} "
            f"Angle={angle:.2f}"
        )

    frame_number += 1

cap.release()

print("\nDetected Angles:")

for i, angle in enumerate(angles):

    print(
        f"Sample {i}: "
        f"{angle:.2f}"
    )

if len(angles) < 2:

    print(
        "FAIL - Not enough motion samples"
    )

    exit()

ccw_count = 0
total_moves = 0

print("\nAngle Deltas:")

for i in range(1, len(angles)):

    previous = angles[i - 1]
    current = angles[i]

    delta = current - previous

    # Handle wraparound
    if delta > 180:
        delta -= 360

    elif delta < -180:
        delta += 360

    total_moves += 1

    direction = "CW/STATIC"

    # For atan2 in image coordinates,
    # negative delta should represent
    # CCW motion in your generated display.
    if delta < 0:

        ccw_count += 1
        direction = "CCW"

    print(
        f"Step {i}: "
        f"Prev={previous:.2f} "
        f"Curr={current:.2f} "
        f"Delta={delta:.2f} "
        f"{direction}"
    )

ratio = ccw_count / total_moves

print("\nSummary")

print(
    f"Total Samples: "
    f"{len(angles)}"
)

print(
    f"Total Moves: "
    f"{total_moves}"
)

print(
    f"CCW Moves: "
    f"{ccw_count}"
)

print(
    f"CCW Ratio: "
    f"{ratio:.2%}"
)

if ratio >= MIN_CCW_RATIO:

    print(
        "PASS - Counter Clockwise Rotation Detected"
    )

else:

    print(
        "FAIL - Counter Clockwise Rotation Not Detected"
    )