import os
import cv2
import time
import base64
from mistralai import Mistral

# Retrieve the API key from environment variables
api_key = os.environ["MISTRAL_API_KEY"]

# Specify model
model = "pixtral-12b-2409"

# Initialize the Mistral client
client = Mistral(api_key=api_key)

# Open the default webcam
cap = cv2.VideoCapture(0)

try:
    while True:
        # Capture a frame
        ret, frame = cap.read()
        
        if ret:
            # Save the frame to a temporary file
            temp_image_path = "/tmp/current_frame.jpg"
            cv2.imwrite(temp_image_path, frame)

            # Convert the image to a base64 string
            with open(temp_image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                base64_image_str = f"data:image/jpeg;base64,{base64_image}"

            # Corrected messages format
            messages = [
                {
                    "role": "user",
                    "content": "What's in this image?",
                },
                {
                    "role": "user",
                    "content": base64_image_str  # Use the base64-encoded image as a string content
                }
            ]

            # Get the chat response
            chat_response = client.chat.complete(
                model=model,
                messages=messages
            )

            # Print the content of the response
            print(chat_response.choices[0].message.content)

        else:
            print("Failed to capture frame")

        # Wait for 10 seconds before capturing the next frame
        time.sleep(10)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Release the capture and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
