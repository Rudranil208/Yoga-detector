# Yoga-detector
Yoga Pose Detection and Classification

This project uses MediaPipe Pose and OpenCV to detect human poses from images and video streams, classify them into various yoga poses, and visualize key angles.

Features

    Real-time Pose Detection: Utilizes MediaPipe Pose to accurately detect 3D body landmarks.

    Angle Calculation: Calculates key joint angles (elbow, shoulder, knee, hip) crucial for pose classification.

    Yoga Pose Classification: Classifies detected poses into several common yoga poses (e.g., Downward Dog, T Pose, Warrior Pose, Tree Pose, Bird Dog Pose, Lotus Pose, Bridge Pose, Cobra Pose).

    Visual Feedback: Displays the detected pose landmarks, calculated angles, and the classified pose label on the output image/video frame.

    Static Image Processing: Ability to process a list of static images to detect and classify poses.

    Live Video Stream Processing: Processes real-time video input from a webcam for continuous pose detection and classification.

Installation

Before running the code, you need to install the required libraries.

    Clone the repository (or download the code):
    Bash

git clone <repository_url>
cd <repository_directory>

(Replace <repository_url> and <repository_directory> with your actual repository details if hosted on GitHub).

Install dependencies:
Bash

    pip install opencv-python mediapipe

Usage

The script can process either static images or a live video stream from your webcam.

1. Preparing Images (for static image processing)

Create a folder named images in the same directory as your script and place your yoga pose images inside it. The example static_image_paths array in the if __name__ == "__main__": block assumes images named img1.jpg to img10.jpg are present.

2. Running the Script

You can run the script from your terminal:
Bash

python your_script_name.py

(Replace your_script_name.py with the actual name of your Python file, e.g., yoga_detector.py)

The if __name__ == "__main__": block in the script demonstrates how to use the functions:

    For Static Images:
    The processStaticImages() function is called with a list of image paths. Uncomment this line if you want to process static images:
    Python

processed_images, labels = processStaticImages(static_image_paths)
# You might want to add code here to display or save the processed_images

Currently, the processed images are stored in processed_images list, but not displayed or saved. You'd need to add cv2.imshow() or cv2.imwrite() calls within the processStaticImages loop or after it to see the results.

For Live Video Stream:
The processVideo() function is called to start the webcam feed. This is enabled by default.
Python

    processVideo()

    Press ESC to exit the video stream window.

Note: By default, both processStaticImages and processVideo are called in the if __name__ == "__main__": block. You might want to comment out one if you only wish to test the other to avoid conflicts or simultaneous execution.

How it Works

    Initialization:

        mp_pose: MediaPipe Pose module for pose estimation.

        mp_drawing: MediaPipe Drawing Utilities for drawing landmarks and connections.

    calculateAngle(landmark1, landmark2, landmark3):

        Takes three landmark coordinates (e.g., shoulder, elbow, wrist) as input.

        Calculates the angle (in degrees) formed by these three points, with landmark2 being the vertex.

    classifyPose(landmarks, output_image):

        Receives a list of detected landmarks and the image frame.

        Extracts specific landmark coordinates.

        Calls calculateAngle for various key joints (elbows, shoulders, knees, hips) to get their respective angles.

        draw_angle helper function is used to visualize these angles on the output_image.

        Contains the core logic for pose classification based on a set of predefined angle ranges for different yoga poses.

        Assigns a label and color based on the classification.

        Draws the label on the output_image.

        Returns the updated image and the classified label.

    detectAndClassifyPose(image, pose):

        Converts the input image from BGR to RGB (MediaPipe prefers RGB).

        Processes the image with pose.process() to get pose landmarks.

        If landmarks are detected:

            Draws the landmarks and connections on the original image using mp_drawing.

            Converts normalized landmark coordinates back to pixel coordinates.

            Calls classifyPose to classify the pose and get the updated image and label.

        Returns the processed image and the label.

    processStaticImages(image_paths):

        Initializes mp_pose in static_image_mode=True.

        Iterates through a list of image file paths.

        Reads each image, processes it with detectAndClassifyPose, and stores the results.

    processVideo():

        Initializes mp_pose in static_image_mode=False for video processing.

        Opens the default webcam (cv2.VideoCapture(0)).

        Enters a loop to continuously read frames from the camera.

        Flips the frame horizontally for a more natural mirror effect.

        Processes each frame with detectAndClassifyPose.

        Displays the processed frame in a window named 'Yoga Pose Detection'.

        Exits the loop if the ESC key (ASCII 27) is pressed.

        Releases the camera and closes all OpenCV windows upon exit.

Pose Classification Logic (Simplified Overview)

The classifyPose function contains a series of if/elif conditions that check the calculated angles to identify specific yoga poses. Each pose has a unique combination of angle ranges for elbows, shoulders, knees, and hips.

Example:

    Downward Dog Pose:

        Elbows relatively straight (140-195 degrees)

        Knees relatively straight (160-195 degrees)

        Hips bent (60-150 degrees or 210-300 degrees, depending on camera angle/direction)

    Warrior Pose:

        One knee bent (90-120 degrees) while the other is relatively straight (165-195 degrees)

The angle ranges are defined based on common representations of these poses. Fine-tuning these ranges might be necessary for better accuracy or to accommodate variations in execution.
