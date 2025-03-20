import cv2

# Load the video
video_path = "videos/sample.mp4"  # Replace with the correct path
video = cv2.VideoCapture(video_path)

# Background subtractor for motion detection
bg_subtractor = cv2.createBackgroundSubtractorMOG2()

# Define two regions of interest (ROI) for Directions A and B
roi_A = (100, 200, 400, 300)  # (x, y, width, height) for Direction A
roi_B = (500, 200, 400, 300)  # (x, y, width, height) for Direction B

def detect_cars(frame, roi):
    """ Detects and counts moving cars in a given region. """
    x, y, w, h = roi
    region = frame[y:y+h, x:x+w]
    
    # Convert to grayscale
    gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    
    # Apply background subtraction
    mask = bg_subtractor.apply(gray)
    
    # Remove noise
    mask = cv2.medianBlur(mask, 5)

    # Detect moving objects
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    car_count = 0
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Ignore small movements (noise)
            car_count += 1

    return car_count

def calculate_green_times(count_A, count_B):
    """ Calculates green light duration based on car counts. """
    total_cars = count_A + count_B
    if total_cars == 0:
        return 30, 30  # Default green time
    
    time_A = (count_A / total_cars) * 60
    time_B = (count_B / total_cars) * 60
    return int(time_A), int(time_B)

# Main loop
while video.isOpened():
    success, frame = video.read()
    if not success:
        break  # Stop if the video ends

    # Detect cars in both directions
    count_A = detect_cars(frame, roi_A)
    count_B = detect_cars(frame, roi_B)

    # Calculate green light durations
    green_time_A, green_time_B = calculate_green_times(count_A, count_B)

    # Display detected car counts
    cv2.putText(frame, f"Direction A: {count_A} cars", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Direction B: {count_B} cars", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Green A: {green_time_A}s", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(frame, f"Green B: {green_time_B}s", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Show the video with car counts
    cv2.imshow("Traffic Detection", frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break  # Exit when 'q' is pressed

video.release()
cv2.destroyAllWindows()

