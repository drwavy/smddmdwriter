import csv
import subprocess
import os


# Helper to write metadata using ExifTool
def write_metadata(file_path, metadata):
    for tag, value in metadata.items():
        cmd = ["exiftool", f"-{tag}={value}", file_path]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Successfully updated {tag} for {file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error writing {tag} to {file_path}: {e}")


# Main function to process the CSV
def process_csv(csv_path, base_dir):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            relative_path = row.get('FilePath')
            if not relative_path:
                continue  # Skip rows with no file path

            # Prepend base_dir to resolve the full file path
            media_path = os.path.join(base_dir, relative_path)

            # Validate that the file exists
            if not os.path.isfile(media_path):
                print(f"File not found: {media_path}")
                continue

            # Metadata to write
            metadata = {}

            # Map CSV columns to metadata tags
            metadata_mapping = {
                "Caption-Abstract": ["IPTC:Caption-Abstract", "XMP:Description"],
                "AllDates": ["DateTimeOriginal", "CreateDate", "ModifyDate",
                             "MediaCreateDate", "MediaModifyDate"],
                "ApertureValue": ["ApertureValue"],
                "CameraElevationAngle": ["CameraElevationAngle"],
                "DateTime": ["DateTime"],
                "DateTimeOriginal": ["DateTimeOriginal"],
                "DeviceSettingDescription": ["DeviceSettingDescription"],
                "FocalLength": ["FocalLength"],
                "ISO": ["ISO"],
                "GPSLatitude": ["GPSLatitude"],
                "LensMake": ["LensMake"],
                "LensModel": ["LensModel"],
                "GPSLongitude": ["GPSLongitude"],
                "MeteringMode": ["MeteringMode"],
                "Genre": ["IPTC:By-line", "IPTC:Credit", "XMP:Creator"],
                "SceneCaptureType": ["SceneCaptureType"],
                "Scene type": ["SceneType"],  # Adjust tag based on intent
                "ShutterSpeedValue": ["ShutterSpeedValue"],
                "Software": ["Software"],
                "FileSource": ["FileSource"]
            }

            # Populate metadata dictionary from the CSV
            for csv_column, tags in metadata_mapping.items():
                value = row.get(csv_column, '').strip()
                if value:
                    for tag in tags:
                        metadata[tag] = value

            # Write all metadata
            if metadata:
                write_metadata(media_path, metadata)


# Run the script
if __name__ == "__main__":
    csv_file_path = "ightml.csv"
    base_dir = input("Enter the base directory for the media files: ").strip()
    process_csv(csv_file_path, base_dir)
