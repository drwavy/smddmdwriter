import csv
import os
import subprocess
from datetime import datetime

def parse_timestamp(timestamp):
    try:
        return datetime.utcfromtimestamp(int(timestamp)).strftime('%Y:%m:%d %H:%M:%S')
    except ValueError:
        try:
            return datetime.strptime(timestamp, '%Y:%m:%d %H:%M:%S').strftime('%Y:%m:%d %H:%M:%S')
        except ValueError:
            return None

def update_metadata_from_csv(csv_file, base_directory, mode):
    missing_files_log = f"missing_files_{mode}.log"
    with open(csv_file, 'r') as file, open(missing_files_log, 'w') as log:
        reader = csv.DictReader(file)
        for row in reader:
            uri = row.get('uri') or row.get('src')
            unix_timestamp = row.get('creation_timestamp')
            latitude = row.get('latitude', None)
            longitude = row.get('longitude', None)
            title_or_sender = row.get('title') if mode == 'content' else row.get('sender_name')

            full_path = os.path.join(base_directory, uri) if uri else None

            if not full_path or not os.path.exists(full_path):
                log.write(f"{full_path}: File not found or missing URI.\n")
                print(f"Skipping {full_path}: File not found or missing URI.")
                continue

            try:
                creation_datetime = parse_timestamp(unix_timestamp) if unix_timestamp else None
            except ValueError:
                log.write(f"{full_path}: Invalid timestamp - {unix_timestamp}\n")
                print(f"Invalid timestamp for {full_path}: {unix_timestamp}")
                continue

            command = [
                "exiftool",
                f"-AllDates={creation_datetime}" if creation_datetime else "",
                f"-FileCreateDate={creation_datetime}" if creation_datetime else "",
                f"-FileModifyDate={creation_datetime}" if creation_datetime else "",
                f"-QuickTime:CreateDate={creation_datetime}" if creation_datetime else "",
                f"-QuickTime:ModifyDate={creation_datetime}" if creation_datetime else "",
                f"-kMDItemContentCreationDate={creation_datetime}" if creation_datetime else "",
                f"-kMDItemContentModificationDate={creation_datetime}" if creation_datetime else "",
                f"-Title={title_or_sender}" if title_or_sender else "",
                f"-Description={title_or_sender}" if title_or_sender else "",
                f"-XPTitle={title_or_sender}" if title_or_sender else "",
                f"-kMDItemDescription={title_or_sender}" if title_or_sender else "",
                f"-kMDItemAuthors={title_or_sender}" if title_or_sender else "",
                f"-GPSLatitude={latitude}" if latitude and mode == 'content' else "",
                f"-GPSLongitude={longitude}" if longitude and mode == 'content' else "",
                full_path
            ]

            command = [arg for arg in command if arg]

            try:
                result = subprocess.run(command, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"Successfully updated metadata for {full_path}")
                else:
                    log.write(f"{full_path}: Error - {result.stderr}\n")
                    print(f"Error updating metadata for {full_path}: {result.stderr}")
            except Exception as e:
                log.write(f"{full_path}: Exception - {str(e)}\n")
                print(f"Exception occurred while processing {full_path}: {e}")


if __name__ == "__main__":
    content_csv_file = "csv/content.csv"
    inbox_csv_file = "csv/inbox.csv"
    base_directory_file = "base_directory.txt"

    if not os.path.exists(base_directory_file):
        print(f"Error: Base directory file '{base_directory_file}' not found.")
    else:
        with open(base_directory_file, 'r') as base_file:
            base_directory = base_file.read().strip()

        if os.path.exists(content_csv_file):
            print("Processing content.csv...")
            update_metadata_from_csv(content_csv_file, base_directory, mode='content')
        else:
            print(f"Error: Content CSV file '{content_csv_file}' not found.")

        if os.path.exists(inbox_csv_file):
            print("Processing inbox.csv...")
            update_metadata_from_csv(inbox_csv_file, base_directory, mode='inbox')
        else:
            print(f"Error: Inbox CSV file '{inbox_csv_file}' not found.")
