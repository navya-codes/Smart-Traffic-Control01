import cv2
import numpy as np

# Path to the saved video file
video_path = "videos/sample2.mp4"

# Open the video file
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Initialize a list to store the red light intensity over time
light_intensity = []

# Set a threshold for detecting flashing lights
flashing_threshold = 5000  # Adjust based on your testing

frame_skip = 5  # Process every 5th frame
frame_count = 0

# Loop to process video frames
while True:
    ret, frame = cap.read()

    if not ret:  # Break if the video ends
        print("Video has ended.")
        break

    frame_count += 1
    if frame_count % frame_skip != 0:
        continue  # Skip this frame and move to the next

    # Convert the frame to HSV for color detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define color range for red lights
    red_lower = np.array([0, 120, 70])
    red_upper = np.array([10, 255, 255])

    # Create a mask for red color
    red_mask = cv2.inRange(hsv, red_lower, red_upper)

    # Count the intensity of the red light in the frame
    red_intensity = cv2.countNonZero(red_mask)  # Number of red pixels

    # Add the intensity to the list
    light_intensity.append(red_intensity)

    # Check if there is enough data to calculate flashing pattern
    if len(light_intensity) > 10:  # Analyze the last 10 frames
        del light_intensity[0]  # Remove the oldest frame's intensity

        # Calculate the change in intensity between consecutive frames
        intensity_changes = [abs(light_intensity[i] - light_intensity[i - 1]) for i in range(1, len(light_intensity))]

        # If the change is above the threshold, it's likely flashing
        if max(intensity_changes) > flashing_threshold:
            print("Flashing red light detected!")

    # Highlight the detected red area in the frame
    red_detected = cv2.bitwise_and(frame, frame, mask=red_mask)

    # Resize the frame for faster processing (optional)
    frame_resized = cv2.resize(red_detected, (640, 480))

    
        

    # Display the results
    cv2.imshow("Flashing Red Light Detection", frame_resized)

    # Wait for a small period before displaying the next frame
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break


# Function to write emergency detection status
def update_emergency_status(detected):
    with open("emergency_detected.txt", "w") as f:
        f.write("1" if detected else "0")

# Example usage inside detection loop:
if red_detected.any():  # If ambulance/fire truck detected
    update_emergency_status(True)
else:
    update_emergency_status(False)


# Release resources and close windows
cap.release()
cv2.destroyAllWindows()