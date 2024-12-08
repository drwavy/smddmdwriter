import pandas as pd
import subprocess
import os
import filetype
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import numpy as np

# Function to format the date
def format_date(date_string):
    try:
        parsed_date = datetime.strptime(date_string, '%b %d, %Y, %I:%M %p')
        return parsed_date.strftime('%Y:%m:%d %H:%M:%S')
    except ValueError:
        return None

# Function to extract additional metadata
def extract_additional_metadata(media_div):
    metadata = {}
    rows = media_div.find_all('tr')
    for row in rows:
        cells = row.find_all('div', class_='_a6-q')
        if len(cells) == 2:
            key, value = cells[0].text.strip(), cells[1].text.strip()
            metadata[key] = value if value.lower() != 'unknown' else None
    return metadata

# Map metadata keys to ExifTool/Apple Photos tag names
metadata_mapping = {
    "Device ID": "DeviceSettingDescription",
    "Camera position": "CameraElevationAngle",
    "Source type": "FileSource",
    "Date taken": "DateTimeOriginal",
    "ISO speed": "ISO",
    "Focal length": "FocalLength",
    "Lens model": "LensModel",
    "Lens make": "LensMake",
    "Date": "DateTime",
    "Aperture": "ApertureValue",
    "Shutter speed": "ShutterSpeedValue",
    "Metering mode": "MeteringMode",
    "Scene capture type": "SceneCaptureType",
    "Latitude": "GPSLatitude",
    "Longitude": "GPSLongitude",
    "Music genre": "Genre",
    "Software": "Software"
}

# Function to rename headers using the mapping
def rename_headers(headers, mapping):
    return [mapping.get(header, header) for header in headers]

# Enhanced function to guess and apply file extensions using filetype library
def guess_and_apply_file_extension_with_filetype(file_path):
    """
    Detects and applies the correct file extension using filetype library.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return file_path

    try:
        kind = filetype.guess(file_path)
        if kind is None:
            print(f"Could not determine file type for {file_path}. Skipping.")
            return file_path

        extension = kind.extension
        new_file_path = f"{file_path}.{extension}"
        os.rename(file_path, new_file_path)
        print(f"Updated file {file_path} with extension .{extension}")
        return new_file_path
    except Exception as e:
        print(f"Error guessing file extension for {file_path}: {e}")
        return file_path

# Function to update missing extensions in the CSV file
def update_missing_extensions_in_csv(csv_path):
    try:
        data = pd.read_csv(csv_path)
        if "FilePath" not in data.columns:
            raise ValueError("The column 'FilePath' is missing in the CSV file.")

        data.replace({np.nan: None}, inplace=True)  # Replace NaN with None

        for index, row in data.iterrows():
            file_path = row['FilePath']
            if not os.path.splitext(file_path)[1]:  # If no file extension
                new_file_path = guess_and_apply_file_extension_with_filetype(file_path)
                data.at[index, 'FilePath'] = new_file_path

        # Save the updated CSV
        data.to_csv(csv_path, index=False)
        print(f"CSV updated with file extensions: {csv_path}")
    except Exception as e:
        print(f"An error occurred while updating file extensions in CSV: {e}")

# Function to process a single HTML file and append data to the CSV
def process_file(file_path, writer, all_metadata_columns):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        main_div = soup.find('div', class_='_a706', role='main')

        post_divs = main_div.find_all('div', class_='pam _3-95 _2ph- _a6-g uiBoxWhite noborder')
        for post_div in post_divs:
            caption_div = post_div.find('div', class_='_3-95 _2pim _a6-h _a6-i')
            caption = caption_div.text if caption_div and caption_div.text.strip() else None

            timestamp_div = post_div.find('div', class_='_3-94 _a6-o')
            raw_timestamp = timestamp_div.text if timestamp_div else None
            formatted_timestamp = format_date(raw_timestamp)

            media_div = post_div.find('div', class_='_3-95 _a6-p')
            if media_div:
                media_links = media_div.find_all('a', href=True)
                metadata = extract_additional_metadata(media_div)
                for media_link in media_links:
                    media_file_path = os.path.join(base_dir, media_link['href'])
                    row = [media_file_path, caption, formatted_timestamp] + [
                        metadata.get(col, None) for col in all_metadata_columns
                    ]
                    writer.writerow(row)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Prompt user for the base directory
base_dir = input("Enter the base directory path: ")

# Files to process
files_to_process = [
    os.path.join(base_dir, 'content', 'archived_posts.html'),
    os.path.join(base_dir, 'content', 'other_content.html'),
    os.path.join(base_dir, 'content', 'profile_photos.html'),
    os.path.join(base_dir, 'content', 'posts_1.html'),
    os.path.join(base_dir, 'content', 'recently_deleted_content.html'),
    os.path.join(base_dir, 'content', 'stories.html')
]
output_csv_path = 'ightml.csv'

# Collect all metadata keys
all_metadata_columns = set()
for file_path in files_to_process:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            main_div = soup.find('div', class_='_a706', role='main')
            post_divs = main_div.find_all('div', class_='pam _3-95 _2ph- _a6-g uiBoxWhite noborder')
            for post_div in post_divs:
                media_div = post_div.find('div', class_='_3-95 _a6-p')
                if media_div:
                    metadata = extract_additional_metadata(media_div)
                    all_metadata_columns.update(metadata.keys())
    except Exception as e:
        print(f"Error collecting metadata keys from {file_path}: {e}")

all_metadata_columns = sorted(all_metadata_columns)
renamed_headers = rename_headers(['FilePath', 'Caption-Abstract', 'AllDates'] + all_metadata_columns, metadata_mapping)

# Write to CSV
with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(renamed_headers)
    for file_path in files_to_process:
        process_file(file_path, writer, all_metadata_columns)

print(f"Parsing complete. Combined CSV file with renamed headers saved at: {output_csv_path}")

# Update missing file extensions in the CSV
update_missing_extensions_in_csv(output_csv_path)

print(f"Missing file extensions updated in CSV.")
