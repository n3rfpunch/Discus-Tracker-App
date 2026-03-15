import cv2
import mediapipe as mp

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Open the video file
video_path = 'C:/Users/n3rfp/Downloads/PXL_20250414_205632185~2.mp4'  # Update the path as needed
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Couldn't open video.")
    exit()

# Get video dimensions
video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # Video width
video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Video height

# Get screen resolution
screen_width = 1920  # Change this to your screen width if needed
screen_height = 1080  # Change this to your screen height if needed

# Calculate the scaling factor while maintaining the aspect ratio
aspect_ratio = video_width / video_height
if video_width > video_height:
    new_width = screen_width
    new_height = int(screen_width / aspect_ratio)
else:
    new_height = screen_height
    new_width = int(screen_height * aspect_ratio)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a selfie-view display
    frame = cv2.flip(frame, 1)

    # Resize the frame to fit the screen size while maintaining aspect ratio
    frame_resized = cv2.resize(frame, (new_width, new_height))

    # Convert the BGR frame to RGB (MediaPipe uses RGB)
    rgb_frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

    # Process the frame and get the pose landmarks
    results = pose.process(rgb_frame)

    # Draw the pose landmarks if they are detected
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame_resized, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Display the resulting frame
    cv2.imshow('Body Position Tracking', frame_resized)

    # Exit the loop when the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
