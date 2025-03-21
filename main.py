#Import Libraries
import cv2
import numpy as np
# Initialize webcam
cap = cv2.VideoCapture(0)
# Error handling for webcam
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()
# Capture the background frame (Wait 2 seconds for stability)
cv2.waitKey(2000)
ret, init_frame = cap.read()
if not ret:
    print("Error: Could not capture background frame.")
    cap.release()
    exit()
# Define HSV range for detecting black color
lower_hsv = np.array([0, 0, 0])      # Lower bound of black color
upper_hsv = np.array([180, 80, 80])  # Upper bound of black color
# Create a kernel for smoothing mask
kernel = np.ones((3,3), np.uint8)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Create a mask for detecting black color
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    mask = cv2.medianBlur(mask, 3)  # Reduce noise
    mask = cv2.dilate(mask, kernel, 5)  # Expand the detected areas
    mask_inv = cv2.bitwise_not(mask)  # Invert mask
    # Extract non-cloak regions from current frame
    frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
    # Extract cloak region from the background frame
    cloak_area = cv2.bitwise_and(init_frame, init_frame, mask=mask)
    # Combine both parts
    final_output = cv2.addWeighted(frame_bg, 1, cloak_area, 1, 0)
    # Display result
    cv2.imshow("Black Cloak Effect", final_output)
    # Press 'q' to exit
    if cv2.waitKey(1) == ord('q'):
        break
# Release resources
cap.release()
cv2.destroyAllWindows()
