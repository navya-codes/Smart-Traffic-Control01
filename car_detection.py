import cv2

# Function to detect and count cars in the video
def detect_and_count_cars(video_path):
    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Background subtractor to detect moving objects
    background_subtractor = cv2.createBackgroundSubtractorMOG2()

    while True:
        # Read each frame from the video
        success, frame = video.read()

        # Check if the video ended
        if not success:
            print("Video finished or cannot read video.")
            break

        # Resize the frame for easier processing
        frame = cv2.resize(frame, (640, 360))

        # Apply the background subtractor
        mask = background_subtractor.apply(frame)

        # Remove noise using simple filter
        mask = cv2.medianBlur(mask, 5)

        # Find the shapes (contours) of moving objects
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        car_count = 0  # Initialize car counter

        # Loop through all the detected contours
        for contour in contours:
            # Ignore small contours that might be noise
            if cv2.contourArea(contour) > 500:
                # Get the rectangle that fits around the contour
                x, y, w, h = cv2.boundingRect(contour)

                # Draw the rectangle on the original frame
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Increase the car count
                car_count += 1

        # Display the car count on the video
        cv2.putText(frame, f"Cars: {car_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Show the original video with rectangles and car count
        cv2.imshow("Car Detection", frame)

        # Show the mask (black and white image)
        #cv2.imshow("Moving Objects", mask)

        # Wait for 30ms and break if 'q' is pressed
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    # Release the video and close all windows
    video.release()
    cv2.destroyAllWindows()


# Run the function directly
video_file = "videos/sample1.mp4"  # Replace with your test video path
detect_and_count_cars(video_file)
