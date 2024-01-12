import os

from motion_capture import extract_motion_data

# Set up the dataset folder path
dataset_folder = "./dataset_trimmed"

# Set up the dataset CSVs folder path
dataset_csvs_folder = "./dataset_csvs"

# Set up the completed videos file path
completed_videos_file = "completed_videos.txt"

# Check if the completed videos file exists
if not os.path.exists(completed_videos_file):
    # Create an empty completed videos file
    with open(completed_videos_file, "w") as file:
        pass

# Function to check if a video has already been processed
def is_video_completed(video_file):
    with open(completed_videos_file, "r") as file:
        completed_videos = file.read().splitlines()
        if video_file in completed_videos:
            return True
        return False

# Function to mark a video as completed
def mark_video_completed(video_file):
    with open(completed_videos_file, "a") as file:
        file.write(video_file + "\n")

# Get a list of all video files in the dataset folder
video_files = [file for file in os.listdir(dataset_folder) if file.endswith(".mp4")]

# Process each video file
for video_file in video_files:
    # Check if the video has already been processed
    if is_video_completed(video_file):
        print(f"Skipping {video_file} - Already processed.")
        continue

    # Get the video file path
    video_path = os.path.join(dataset_folder, video_file)

    # Create the output CSV file path
    output_csv_path = os.path.join(dataset_csvs_folder, os.path.splitext(video_file)[0] + ".csv")

    # Process the video and extract motion data
    extract_motion_data(video_path, output_csv_path)

    # Mark the video as completed
    mark_video_completed(video_file)

    print(f"Processed {video_file} - Motion data extracted and saved to {output_csv_path}.")
