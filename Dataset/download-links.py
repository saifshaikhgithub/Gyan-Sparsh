import json
from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import datetime
import os


ORIGINAL_PATH = "./dataset_original/"
TRIMMED_PATH = "./dataset_trimmed/"
DATABASE_PATH = "./database-complete.txt"

# Load the dataset links from the JSON file
with open("./download-links.json") as f:
    dataset_links = json.load(f)

# mkdir if not exists
if not os.path.exists(ORIGINAL_PATH):
    os.makedirs(ORIGINAL_PATH)

if not os.path.exists(TRIMMED_PATH):
    os.makedirs(TRIMMED_PATH)

if not os.path.exists(DATABASE_PATH):
    open(DATABASE_PATH, 'w').close()

# Load the processed video links from the database file
if os.path.exists(DATABASE_PATH):
    with open(DATABASE_PATH, "r") as f:
        processed_links = set(line.strip() for line in f)
else:
    processed_links = set()

for video_name, video_data in dataset_links.items():
    video_link = video_data["link"]
    start_time = video_data["start_time"]
    end_time = video_data["end_time"]


    # Check if this video has already been processed
    if video_link in processed_links:
        print(f"Skipping {video_name}, already processed.")
        continue

    try:
        yt = YouTube(video_link, use_oauth=True)
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        video_path = video.download(output_path=ORIGINAL_PATH)

        print(f"Downloaded {video_name}: {yt.title}")

        # Convert start and end times to seconds
        start = datetime.datetime.strptime(start_time, '%M:%S.%f')
        end = datetime.datetime.strptime(end_time, '%M:%S.%f')
        start_seconds = (start - datetime.datetime(1900, 1, 1)).total_seconds()
        end_seconds = (end - datetime.datetime(1900, 1, 1)).total_seconds()

        # Trim the video and save it
        output_path = f"{TRIMMED_PATH}{video_name}.mp4"
        ffmpeg_extract_subclip(video_path, start_seconds, end_seconds, targetname=output_path)

        print(f"Trimmed {video_name} from {start_time} to {end_time}: {output_path}")

        # Mark this video as processed in the database file
        with open(DATABASE_PATH, "a") as f:
            f.write(f"{video_link}\n")
    except Exception as e:
        print(f"Error processing {video_name}: {e}")
