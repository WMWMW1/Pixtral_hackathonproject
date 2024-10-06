# nodes/camera_capture_node.py
import os
from PyQt5.QtWidgets import (
    QLabel, QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage
from nodes.main_window import clear_layout
import cv2

def create_camera_capture_node(layout, next_node=None, button_text="Capture", model="pixtral-12b-2409", image_storage_path="../images"):
    """
    Create a node that allows users to capture photos using the webcam and save them locally.

    :param layout: Main layout to add the camera interface.
    :param next_node: Callback function after capturing the image, passing the image file path.
    :param button_text: Text for the capture button.
    :param model: Model to use for image understanding.
    :param image_storage_path: Local path to store captured images.
    """
    # Clear current layout
    clear_layout(layout)

    # Create a QLabel to display the webcam feed
    video_label = QLabel()
    video_label.setAlignment(Qt.AlignCenter)
    video_label.setFixedSize(500, 400)  # Limit webcam display size

    # Create buttons
    capture_button = QPushButton(button_text if button_text else "Capture")
    retake_button = QPushButton("Retake")
    retake_button.setVisible(False)  # Initially hidden
    delete_button = QPushButton("Delete")
    delete_button.setVisible(False)  # Initially hidden
    confirm_button = QPushButton("Confirm")
    confirm_button.setVisible(False)  # Initially hidden

    # Layout for buttons
    button_layout = QHBoxLayout()
    button_layout.addWidget(capture_button)
    button_layout.addWidget(retake_button)
    button_layout.addWidget(delete_button)
    button_layout.addWidget(confirm_button)

    # Main vertical layout
    vbox = QVBoxLayout()
    vbox.addWidget(video_label)
    vbox.addLayout(button_layout)

    layout.addLayout(vbox)

    # Open the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        video_label.setText("Cannot access webcam")
        return

    # Timer to update video frames
    timer = QTimer()

    # Function to update video frames
    def update_frame():
        ret, frame = cap.read()
        if ret:
            # Convert image to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert to Qt format
            height, width, channel = frame_rgb.shape
            bytes_per_line = 3 * width
            qimg = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            # Scale image to fit QLabel
            scaled_qimg = qimg.scaled(500, 400, Qt.KeepAspectRatio)
            # Display image
            video_label.setPixmap(QPixmap.fromImage(scaled_qimg))
        else:
            video_label.setText("Cannot read frame")

    # Start the timer to update frames
    timer.timeout.connect(update_frame)
    timer.start(30)  # Update every 30 ms

    captured_image = {'image': None}  # To store the captured image

    # Function to capture image
    def capture_image():
        # Stop the timer
        timer.stop()
        # Read the current frame
        ret, frame = cap.read()
        if ret:
            # Store the captured image
            captured_image['image'] = frame.copy()
            # Convert to RGB and display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame_rgb.shape
            bytes_per_line = 3 * width
            qimg = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            scaled_qimg = qimg.scaled(500, 400, Qt.KeepAspectRatio)
            video_label.setPixmap(QPixmap.fromImage(scaled_qimg))
            # Update button visibility
            capture_button.setVisible(False)
            retake_button.setVisible(True)
            delete_button.setVisible(True)
            confirm_button.setVisible(True)
        else:
            video_label.setText("Failed to capture image")

    # Function to retake image
    def retake_image():
        # Restart the timer
        timer.start(30)
        # Clear the captured image
        captured_image['image'] = None
        # Update button visibility
        capture_button.setVisible(True)
        retake_button.setVisible(False)
        delete_button.setVisible(False)
        confirm_button.setVisible(False)

    # Function to delete image
    def delete_image():
        # Stop the timer
        timer.stop()
        # Clear the captured image
        captured_image['image'] = None
        # Display message
        video_label.setText("Image deleted. Please retake.")
        # Update button visibility
        capture_button.setVisible(True)
        retake_button.setVisible(False)
        delete_button.setVisible(False)
        confirm_button.setVisible(False)

    # Function to confirm image capture
    def confirm_image():
        # Ensure image storage directory exists
        if not os.path.exists(image_storage_path):
            os.makedirs(image_storage_path)
        
        # Define image path
        image_path = os.path.join(image_storage_path, "captured_image.jpg")

        # Save image to file
        if captured_image['image'] is not None:
            cv2.imwrite(image_path, captured_image['image'])
            print(f"Image saved to: {image_path}")

        # Release webcam and stop timer
        cap.release()
        timer.stop()
        # Call the next node with the image path
        if next_node:
            next_node(image_path)

    # Connect button events
    capture_button.clicked.connect(capture_image)
    retake_button.clicked.connect(retake_image)
    delete_button.clicked.connect(delete_image)
    confirm_button.clicked.connect(confirm_image)

    # Release resources when the window is closed
    def release_resources():
        cap.release()
        timer.stop()

    video_label.destroyed.connect(release_resources)
