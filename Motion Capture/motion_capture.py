import mediapipe as mp
import cv2
import csv

# Initialize MediaPipe Holistic model
mp_holistic = mp.solutions.holistic


# Define function to extract motion data from video
def extract_motion_data(video_path, output_csv_path):
    # Initialize video capture
    cap = cv2.VideoCapture(video_path)

    # Initialize MediaPipe Holistic model
    with mp_holistic.Holistic(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as holistic:
        # Initialize output CSV file
        with open(output_csv_path, mode="w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            POSES = 33
            HANDS = 21
            FACE = 468

            header_list = ["Frame"]

            for i in range(POSES):
                header_list.append(f"Pose_{i}")
            for i in range(HANDS):
                header_list.append(f"Left_Hand_{i}")
            for i in range(HANDS):
                header_list.append(f"Right_Hand_{i}")
            for i in range(FACE):
                header_list.append(f"Face_{i}")

            csv_writer.writerow(header_list)

            # Process each frame of the video
            frame_num = 0
            while cap.isOpened():
                # Read frame from video
                ret, frame = cap.read()

                if not ret:
                    break

                # Convert frame to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Process frame with MediaPipe Holistic model
                results = holistic.process(frame)


                motion_row_list = [frame_num]

                if results.pose_landmarks:
                    for pose in results.pose_landmarks.landmark:
                        motion_row_list.append(pose)
                else:
                    for _ in range(POSES):
                        motion_row_list.append("-")

                if results.left_hand_landmarks:
                    for left_hand in results.left_hand_landmarks.landmark:
                        motion_row_list.append(left_hand)
                else:
                    for _ in range(HANDS):
                        motion_row_list.append("-")

                if results.right_hand_landmarks:
                    for right_hand in results.right_hand_landmarks.landmark:
                        motion_row_list.append(right_hand)
                else:
                    for _ in range(HANDS):
                        motion_row_list.append("-")

                if results.face_landmarks:
                    for face in results.face_landmarks.landmark:
                        motion_row_list.append(face)
                else:
                    for _ in range(FACE):
                        motion_row_list.append("-")

                csv_writer.writerow(motion_row_list)


                frame_num += 1

    # Release video capture
    cap.release()


