from flask import Flask, Response
from flask_cors import CORS
import cv2
import mediapipe as mp
from yogatrainer2 import detectAndClassifyPose

# Initialize Mediapipe Pose
mp_pose = mp.solutions.pose
pose_video = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)

app = Flask(__name__)
CORS(app)

# Initialize webcam
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        frame, label = detectAndClassifyPose(frame, pose_video)
        _, buffer = cv2.imencode('.jpg', frame)
        frame_encoded = buffer.tobytes()

        # Return video stream with label overlay
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_encoded + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)