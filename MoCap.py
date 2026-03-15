import cv2
import mediapipe as mp

class BodyTracker:
    def __init__(self, camera_index = 1):
        # Initialize camera capture and MediaPipe pose estimation model
        self.cap = cv2.VideoCapture(camera_index)
        self.pose = mp.solutions.pose.Pose()
        self.mp_draw = mp.solutions.drawing_utils

    def track_joints(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            # Convert the image to RGB as MediaPipe requires RGB images
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb_frame)

            # Draw pose landmarks if detected
            if results.pose_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, 
                    results.pose_landmarks, 
                    mp.solutions.pose.POSE_CONNECTIONS
                )

                # Extract landmark coordinates
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(frame, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
                    # Print or process joint coordinates as needed
                    print(f"Joint {id}: (x: {cx}, y: {cy})")

            # Display the output frame
            cv2.imshow("Body Tracker", frame)

            # Break loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release resources
        self.cap.release()
        cv2.destroyAllWindows()

# Usage
if __name__ == "__main__":
    tracker = BodyTracker()
    tracker.track_joints()