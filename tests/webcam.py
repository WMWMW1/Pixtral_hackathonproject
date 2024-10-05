import cv2
import time
import os

# Define the relative directory where you want to save the images
save_directory = "./image"  # Saves images in the current working directory

# Open the default webcam (index 0)
cap = cv2.VideoCapture(0)

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Allow the camera to warm up for a second before capturing the first frame
time.sleep(1)

# Capture a frame every 10 seconds
try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # If the frame is captured successfully, display it
        if ret:
            cv2.imshow('Webcam Feed', frame)

            # Save a frame every 10 seconds
            timestamp = int(time.time())
            image_filename = os.path.join(save_directory, f"frame_{timestamp}.jpg")
            cv2.imwrite(image_filename, frame)
            print(f"Captured and saved frame: {image_filename}")

            # Wait for 10 seconds before capturing the next frame
            time.sleep(10)

        else:
            print("Error: Could not read frame.")
            break

        # Check if 'q' key is pressed to break the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Release the capture and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
