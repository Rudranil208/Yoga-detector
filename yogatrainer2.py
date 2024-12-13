import cv2
import mediapipe as mp
import math

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Function to calculate the angle between three points
def calculateAngle(landmark1, landmark2, landmark3):
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3

    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    if angle < 0:
        angle += 360
    return angle

# Function to classify yoga pose
def classifyPose(landmarks, output_image):
    label = "Unknown Pose"
    color = (0, 0, 255)  # Red for unknown
    
    # Helper to draw angle and lines
    def draw_angle(image, point1, point2, point3, angle, color):
        # Draw lines between points
        cv2.line(image, point1[:2], point2[:2], color, 2)
        cv2.line(image, point2[:2], point3[:2], color, 2)
        
        # Display the angle near the middle point
        mid_point = (point2[0], point2[1] - 20)  # Offset upward
        cv2.putText(image, f"{int(angle)}°", mid_point, cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Calculate angles
    left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
    right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])
    left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])
    
    
    right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])
    
    left_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])
    right_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])

    # Calculate hip angles
    left_hip_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER],
                                    landmarks[mp_pose.PoseLandmark.LEFT_HIP],
                                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE])
    right_hip_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER],
                                        landmarks[mp_pose.PoseLandmark.RIGHT_HIP],
                                        landmarks[mp_pose.PoseLandmark.RIGHT_KNEE])

    # Draw angles on the image
    
    draw_angle(output_image,
               landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
               landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
               landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value],
               left_elbow_angle, (0, 255, 0))  # Green

    draw_angle(output_image,
               landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
               landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
               landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value],
               right_elbow_angle, (0, 255, 0))  # Green

    draw_angle(output_image,
               landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
               landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
               landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value],
               left_knee_angle, (255, 0, 0))  # Blue

    draw_angle(output_image,
               landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
               landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
               landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value],
               right_knee_angle, (255, 0, 0))  # Blue

    draw_angle(output_image,
             landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
             landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
             left_shoulder_angle, (255, 255, 0))  # Cyan

    draw_angle(output_image,
             landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
             landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
             landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
             right_shoulder_angle, (255, 255, 0))  # Cyan

    draw_angle(output_image,
             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
             landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
             landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
             left_hip_angle, (0, 0, 255))  # Red

    draw_angle(output_image,
             landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
             landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
             landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
             right_hip_angle, (0, 0, 255))  # Red

   
    if 140 < left_elbow_angle < 195 and 150 < right_elbow_angle < 210:
        if (160 < left_knee_angle < 195 and 160 < right_knee_angle < 195):
            if((60<=right_hip_angle<=150 and 60<=left_hip_angle<=150) or (210<=right_hip_angle<=300 and 210<=left_hip_angle<=300)):
                label = "Downward Dog Pose"
                color = (75,0,130) #indigo
            if((210<=left_hip_angle<=300 and 120<=right_hip_angle<=200)or(60<=right_hip_angle<=150 and 160<=left_hip_angle<=240)):
                label = "T Pose"
                color = (255, 0, 255)  # Purple
        elif(90 < left_knee_angle < 120 or 90 < right_knee_angle < 120) and \
            (165 < left_knee_angle < 195 or 165 < right_knee_angle < 195):
            label = "Warrior Pose"
            color = (255, 255, 0)  # Yellow
        elif((310 <= left_knee_angle <= 350 and 150 <= right_knee_angle <= 210) or 
            (20 <= right_knee_angle <=80 and 150 <= left_knee_angle <= 210)):
            label = "Tree Pose"
            color = (0, 255, 0) # Green
        elif((250<=left_knee_angle<=300 and 150<=right_knee_angle<=200) or \
            (250<=right_knee_angle<=300 and 150<=left_knee_angle<=200)):
            label = "Bird Dog Pose"
            color=(255,70,200) # pink
        elif(10<=right_knee_angle<=30 and 260<=left_knee_angle<=360):
            label = "Lotus Pose"
            color= (255,0,0) #red
        elif((250<=right_knee_angle<=300 and 250<=left_knee_angle<=300) or \
            (60<=right_knee_angle<=100 and 60<=left_knee_angle<=100)):
            label = "Bridge Pose"
            color = (0,0,255) #blue
        #elif(((120<=right_hip_angle<=150 and 120<=left_hip_angle<=150) or (210<=right_hip_angle<=240 and 210<=left_hip_angle<=240))):
            
    if(140<=right_elbow_angle<=210 and 140<=left_elbow_angle<=210):
        if((120<=right_hip_angle<=150 and 120<=left_hip_angle<=150) or (210<=right_hip_angle<=250 and 210<=left_hip_angle<=250)):
            label = "Cobra Pose"
            color = (150,75,0) #brown

    # Display label on the image
    cv2.putText(output_image, label, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

    # Pose classification logic here
    # (Same logic as in your original code)
    # Return updated image and label
    return output_image, label

# Function to detect and classify pose
def detectAndClassifyPose(image, pose):
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(imageRGB)
    height, width, _ = image.shape
    landmarks = []

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=results.pose_landmarks,
            connections=mp_pose.POSE_CONNECTIONS
        )
        for landmark in results.pose_landmarks.landmark:
            landmarks.append((int(landmark.x * width), int(landmark.y * height), (landmark.z * width)))
        output_image, label = classifyPose(landmarks, image)
        return output_image, label

    return image, "No Pose Detected"

# Function for static image processing
def processStaticImages(image_paths):
    pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5, model_complexity=2)
    processed_images = []
    labels = []

    for img_path in image_paths:
        sample_img = cv2.imread(img_path)
        if sample_img is not None:
            output_img, label = detectAndClassifyPose(sample_img, pose)
            processed_images.append(output_img)
            labels.append(label)
        else:
            print(f"Error: Could not read the image file at {img_path}. Check the file path.")
    return processed_images, labels

# Function for video processing
def processVideo():
    pose_video = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)
    camera_video = cv2.VideoCapture(0)
    cv2.namedWindow('Yoga Pose Detection', cv2.WINDOW_NORMAL)

    while camera_video.isOpened():
        ok, frame = camera_video.read()
        if not ok:
            break
        frame = cv2.flip(frame, 1)
        frame, label = detectAndClassifyPose(frame, pose_video)
        cv2.imshow('Yoga Pose Detection', frame)
        if cv2.waitKey(1) & 0xFF == 27:  # Exit on pressing ESC
            break

    camera_video.release()
    cv2.destroyAllWindows()

# Only execute this block if script is run directly
if __name__ == "__main__":
    # Example usage
    static_image_paths = [
        'images\img1.jpg',
        'images\img2.jpg',
        'images\img3.jpg',
        'images\img4.jpg',
        'images\img5.jpg',
        'images\img6.jpg',
        'images\img7.jpg',
        'images\img8.jpg',
        'images\img9.jpg',
        'images\img10.jpg'
    ]
    # Uncomment the function you want to test
    processed_images, labels = processStaticImages(static_image_paths)
    processVideo()
