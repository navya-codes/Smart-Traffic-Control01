import cv2
import numpy as np

# Path to the saved video file
video_path = "videos/sample.mp4"  

# Open the video file
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# List to store red light intensity over time
light_intensity = []

# Threshold for detecting flashing lights
flashing_threshold = 5000  # Adjust based on testing

frame_skip = 5  # Process every 5th frame
frame_count = 0

# Loop to process video frames
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:  # Break if the video ends
        print("Video has ended.")
        break

    frame_count += 1
    if frame_count % frame_skip != 0:
        continue  # Skip frames for efficiency

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define red color range
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])

    # Create a mask for red color detection
    red_mask = cv2.inRange(hsv, lower_red, upper_red)

    # Count red light intensity
    red_intensity = cv2.countNonZero(red_mask)

    # Store intensity in the list
    light_intensity.append(red_intensity)

    # Keep only the last 10 frames for analysis
    if len(light_intensity) > 10:
        light_intensity.pop(0)  # Remove the oldest frame's intensity

        # Calculate the change in intensity between frames
        intensity_changes = [abs(light_intensity[i] - light_intensity[i - 1]) for i in range(1, len(light_intensity))]

        # If the change is above the threshold, it's likely flashing
        if max(intensity_changes) > flashing_threshold:
            print("🚨 Flashing red light detected! Possible emergency vehicle.")

    # Highlight detected red areas in the frame
    red_detected = cv2.bitwise_and(frame, frame, mask=red_mask)

    # Resize the frame for faster processing
    frame_resized = cv2.resize(red_detected, (640, 480))

    # Show the detected flashing red light
    cv2.imshow("Emergency Light Detection", frame_resized)

    # Wait for a small period before displaying the next frame
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release resources and close windows
cap.release()
cv2.destroyAllWindows()
