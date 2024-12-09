import csv
import subprocess
from datetime import datetime
import os


# Helper to format timestamp for EXIF (YYYY:MM:DD HH:MM:SS)
def format_timestamp_exif(timestamp):
    dt = datetime.strptime(timestamp, "%b %d, %Y, %I:%M %p")
    return dt.strftime("%Y:%m:%d %H:%M:%S")


# Convert AAC to M4A using ffmpeg
def convert_aac_to_m4a(aac_path):
    m4a_path = aac_path.replace(".aac", ".m4a")
    cmd = ["ffmpeg", "-i", aac_path, m4a_path]
    try:
        subprocess.run(cmd, check=True)
        print(f"Converted {aac_path} to {m4a_path}")
        return m4a_path
    except subprocess.CalledProcessError as e:
        print(f"Error converting {aac_path} to M4A: {e}")
        return None


# Helper to write metadata using ExifTool
def write_metadata(file_path, metadata):
    for tag, value in metadata.items():
        cmd = ["exiftool", f"-{tag}={value}", file_path]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error writing metadata to {file_path}: {e}")
            return


# Main function to process CSV
def process_csv(csv_path, base_dir):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            relative_path = row.get('Message Content Media Item Path')
            if not relative_path:
                continue  # Skip rows with no media path

            # Prepend base_dir to relative file path
            media_path = os.path.join(base_dir, relative_path)

            # Validate the full file path exists
            if not os.path.isfile(media_path):
                print(f"File not found: {media_path}")
                continue

            media_type = row.get('Message Content Media Item Type')
            timestamp = row.get('Timestamp')
            if not timestamp or not media_type:
                continue  # Skip rows with missing data

            formatted_timestamp = format_timestamp_exif(timestamp)
            metadata = {}

            # Handle Images
            if media_type == 'img':
                metadata = {
                    "DateTimeOriginal": formatted_timestamp,
                    "CreateDate": formatted_timestamp,
                    "ModifyDate": formatted_timestamp,
                    "MediaCreateDate": formatted_timestamp,
                    "MediaModifyDate": formatted_timestamp,
                    "XMP:DateCreated": formatted_timestamp,
                    "XMP:ModifyDate": formatted_timestamp
                }
            # Handle Videos
            elif media_type == 'video':
                metadata = {
                    "CreationDate": formatted_timestamp,
                    "TrackCreateDate": formatted_timestamp,
                    "TrackModifyDate": formatted_timestamp,
                    "MediaCreateDate": formatted_timestamp,
                    "MediaModifyDate": formatted_timestamp,
                    "DateTimeOriginal": formatted_timestamp
                }
            # Handle Audio
            elif media_type == 'audio':
                # Convert AAC to M4A if needed
                if media_path.endswith(".aac"):
                    media_path = convert_aac_to_m4a(media_path)
                    if not media_path:
                        continue  # Skip if conversion failed

                metadata = {
                    "CreationDate": formatted_timestamp,
                    "MediaCreateDate": formatted_timestamp,
                    "MediaModifyDate": formatted_timestamp,
                }

            # Write metadata to the file
            write_metadata(media_path, metadata)


# Run the script
if __name__ == "__main__":
    csv_file_path = "ightmlmsg.csv"
    base_dir = input("Enter the base directory for the media files: ").strip()
    process_csv(csv_file_path, base_dir)
