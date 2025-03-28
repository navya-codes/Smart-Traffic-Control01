import cv2
import numpy as np

# Global variable to store car count
current_car_count = 0

# Function to detect and count cars in the video
def detect_and_count_cars(video_path):
    global current_car_count  # Use global variable to store car count
    
    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Background subtractor to detect moving objects
    background_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)

    total_car_count = 0  # Total unique cars detected
    min_area = 1200  # Minimum contour area to consider as a car
    tracking_threshold = 40  # Distance threshold to determine new cars

    previous_cars = []  # Stores previous frame cars (center positions)

    while True:
        # Read each frame from the video
        success, frame = video.read()
        if not success:
            break  # Stop processing if video ends

        # Resize frame for easier processing
        frame = cv2.resize(frame, (640, 360))

        # Apply the background subtractor
        fg_mask = background_subtractor.apply(frame)

        # Apply morphological operations to clean noise
        kernel = np.ones((5, 5), np.uint8)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)

        # Find contours of moving objects
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        current_cars = []  # To track cars in the current frame

        for contour in contours:
            if cv2.contourArea(contour) > min_area:
                # Get bounding box for detected vehicle
                x, y, w, h = cv2.boundingRect(contour)
                cx, cy = x + w // 2, y + h // 2  # Find center of the detected car

                # Draw rectangle around detected car
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Store center positions of cars
                current_cars.append((cx, cy))

        # Compare current frame cars with previous frame cars
        new_cars = 0  # Count newly detected cars
        for car in current_cars:
            # If a car is far from previously detected ones, count it as a new car
            if not any(abs(car[0] - prev[0]) < tracking_threshold and abs(car[1] - prev[1]) < tracking_threshold for prev in previous_cars):
                new_cars += 1  # Count new car

        total_car_count += new_cars  # Update total count
        previous_cars = current_cars  # Update previous frame cars for tracking

        # Update the global car count variable
        current_car_count = len(current_cars)
        

        # Display counts on video
        cv2.putText(frame, f"Cars in Frame: {current_car_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Total Cars: {total_car_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Show processed video
        cv2.imshow("Car Detection", frame)

        # Write the current car count to a file
        try:
            with open("car_count.txt", "w") as f:
                f.write(str(current_car_count)) 
                print(f"Updated car count: {current_car_count}") # Use global car count variable
        except Exception as e:
            print(f"Error writing to file:{e}")


        # Exit when 'q' is pressed
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    # Release video and close windows
    video.release()
    cv2.destroyAllWindows()

    return total_car_count  # Return the total count so it can be used elsewhere


# Run the function
video_file = "videos/sample2.mp4"  # Update with your video file path
car_count = detect_and_count_cars(video_file)

# Now the car_count variable stores the count and can be used in other parts of the system
print(f"Final total cars detected: {car_count}")
