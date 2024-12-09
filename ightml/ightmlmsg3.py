import csv
import subprocess
import os


# Helper to write metadata using ExifTool
def write_caption(file_path, caption):
    metadata = {
        "IPTC:Caption-Abstract": caption,
        "XMP:Description": caption
    }
    for tag, value in metadata.items():
        cmd = ["exiftool", f"-{tag}={value}", file_path]
        try:
            subprocess.run(cmd, check=True)
            print(f"Successfully updated {tag} for {file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error writing {tag} to {file_path}: {e}")


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

            # Get the caption
            caption = row.get('Message Content', '').strip()
            if not caption:
                print(f"No caption found for {media_path}, skipping.")
                continue

            # Write caption to metadata
            write_caption(media_path, caption)


# Run the script
if __name__ == "__main__":
    csv_file_path = "ightmlmsg.csv"
    base_dir = input("Enter the base directory for the media files: ").strip()
    process_csv(csv_file_path, base_dir)
