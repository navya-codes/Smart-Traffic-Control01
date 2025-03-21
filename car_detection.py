import cv2

def detect_and_count_cars(video_path):
    # Open the video file
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    # Background subtractor to detect moving objects
    background_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)

    # Morphological kernel for noise reduction
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    total_car_count = 0  # Total cars counted in the video
    tracked_cars = []  # List to store positions of tracked cars

    while True:
        # Read each frame from the video
        success, frame = video.read()
        if not success:
            break

        # Resize the frame for easier processing
        frame = cv2.resize(frame, (640, 360))

        # Apply the background subtractor
        mask = background_subtractor.apply(frame)

        # Remove noise using morphological operations
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.medianBlur(mask, 5)

        # Find the shapes (contours) of moving objects
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        current_frame_cars = []  # Cars detected in the current frame

        # Loop through all the detected contours
        for contour in contours:
            # Ignore small contours that might be noise
            if cv2.contourArea(contour) < 500:
                continue

            # Get the rectangle that fits around the contour
            x, y, w, h = cv2.boundingRect(contour)

            # Filter based on aspect ratio to exclude non-car objects
            aspect_ratio = w / h
            if 1.2 < aspect_ratio < 4.5:  # Adjusted aspect ratio for cars
                current_frame_cars.append((x, y, w, h))

        # Track cars and avoid double counting
        for (x, y, w, h) in current_frame_cars:
            is_new_car = True
            for i, (tx, ty, tw, th) in enumerate(tracked_cars):
                # Check if the current car overlaps with a tracked car
                if abs(x - tx) < tw and abs(y - ty) < th:
                    is_new_car = False
                    # Update the tracked car's position
                    tracked_cars[i] = (x, y, w, h)
                    break

            if is_new_car:
                # Add the car to the tracked list
                tracked_cars.append((x, y, w, h))
                total_car_count += 1

        # Draw rectangles and update the display
        for (x, y, w, h) in current_frame_cars:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the total car count on the video
        cv2.putText(frame, f"Total Cars: {total_car_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Show the processed frame
        cv2.imshow("Car Detection", frame)

        # Wait for 30ms and break if 'q' is pressed
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    # Release the video and close all windows
    video.release()
    cv2.destroyAllWindows()

    # Print final car count after video ends
    print(f"Total cars detected in the entire video: {total_car_count}")


# Run the function directly
video_file = "videos/sample.mp4"  # Replace with your test video path
detect_and_count_cars(video_file)