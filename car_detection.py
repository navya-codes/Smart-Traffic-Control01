import cv2
import numpy as np

# Load video
video_path = "sample.mp4"  # Change this to your video file path
cap = cv2.VideoCapture(video_path)

# Create Background Subtractor
bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)

# Kernel for noise reduction
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

# Car count
total_cars = 0
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # Stop if the video ends
    
    frame_count += 1  # Track frame number
    
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply background subtraction
    fgmask = bg_subtractor.apply(gray)

    # Remove noise
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    # Find contours
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    car_count = 0  # Cars detected in this frame

    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Ignore small objects
            car_count += 1
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    total_cars += car_count  # Update total count

    # Display frame with detections
    cv2.putText(frame, f"Frame {frame_count}: Cars = {car_count}", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
    cv2.imshow("Car Detection", frame)
    cv2.imshow("Foreground Mask", fgmask)

    print(f"Frame {frame_count}: Cars detected = {car_count}")  # Debugging info

    # Exit if 'q' is pressed
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print(f"Total cars detected in the entire video: {total_cars}")
