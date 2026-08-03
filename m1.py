## Milestone 1 - Basic Image Matching
import cv2

reference = cv2.imread("images/good.png", cv2.IMREAD_GRAYSCALE)
test = cv2.imread("images/good.png", cv2.IMREAD_GRAYSCALE)

result = cv2.matchTemplate(test, reference, cv2.TM_CCOEFF_NORMED)

score = result.max()

print(f"Match Score: {score:.3f}")

if score > 0.90:
    print("MATCH")
else:
    print("NO MATCH")