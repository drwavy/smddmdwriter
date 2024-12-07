import csv
import subprocess
import logging
import os

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def apply_metadata_with_ffmpeg(source_file, metadata):
    try:
        cmd = [
            'ffmpeg', '-i', source_file,
            '-metadata', f"title={metadata['Keyword']}",
            '-metadata', f"date={metadata['AllDates']}",
            '-codec', 'copy', f"{source_file}_temp.aac"
        ]
        subprocess.run(cmd, check=True)

        os.replace(f"{source_file}_temp.aac", source_file)
        logging.info(f"Successfully applied metadata to {source_file} using ffmpeg")

    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to apply metadata with ffmpeg for {source_file}: {e}")

with open('csv/messages_media.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        source_file = row['SourceFile']

        if source_file.startswith("https://") or source_file.startswith("http://"):
            logging.info(f"Skipping file with URL: {source_file}")
            continue

        try:
            result = subprocess.run(
                ['exiftool', '-m', '-overwrite_original_in_place', f"-AllDates={row['AllDates']}", source_file],
                check=True, capture_output=True, text=True
            )
            logging.info(f"Successfully applied AllDates to {source_file} using exiftool: {result.stdout.strip()}")

        except subprocess.CalledProcessError as e:
            if "Not a valid AAC" in str(e.stderr):
                logging.warning(f"Exiftool failed for {source_file}, attempting to use ffmpeg.")
                apply_metadata_with_ffmpeg(source_file, {'Keyword': row['Keyword'], 'AllDates': row['AllDates']})
            else:
                logging.error(f"Error applying AllDates to {source_file} with exiftool: {e.stderr.strip()}")
                continue

        try:
            result = subprocess.run(
                ['exiftool', '-m', '-overwrite_original_in_place', f"-Keyword={row['Keyword']}", source_file],
                check=True, capture_output=True, text=True
            )
            logging.info(f"Successfully applied Keyword to {source_file} using exiftool: {result.stdout.strip()}")

        except subprocess.CalledProcessError as e:
            if "Not a valid AAC" in str(e.stderr):
                logging.warning(f"Exiftool failed for {source_file}, attempting to use ffmpeg for Keyword.")
                apply_metadata_with_ffmpeg(source_file, {'Keyword': row['Keyword'], 'AllDates': row['AllDates']})
            else:
                logging.error(f"Error applying Keyword to {source_file} with exiftool: {e.stderr.strip()}")
