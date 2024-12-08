import csv
import subprocess
import os
import locale

# Metadata mapping dictionary with Apple Photos XMP tags
metadata_mapping = {
    "FilePath": {"ExifTool": "FileName"},
    "Caption-Abstract": {"ExifTool": ["Caption-Abstract", "XMP-dc:Description"]},
    "AllDates": {"ExifTool": ["DateTimeOriginal", "ModifyDate", "CreateDate"]},
    "ApertureValue": {"ExifTool": "ApertureValue"},
    "CameraElevationAngle": {"ExifTool": "XMP:CameraPosition"},
    "DateTime": {"ExifTool": "ModifyDate"},
    "DateTimeOriginal": {"ExifTool": ["DateTimeOriginal", "XMP-photoshop:DateCreated"]},
    "DeviceSettingDescription": {"ExifTool": "XMP:DeviceID"},
    "FocalLength": {"ExifTool": "FocalLength"},
    "ISO": {"ExifTool": "ISO"},
    "GPSLatitude": {"ExifTool": "GPSLatitude"},
    "LensMake": {"ExifTool": "LensMake"},
    "LensModel": {"ExifTool": ["LensModel", "XMP-exif:LensModel"]},
    "GPSLongitude": {"ExifTool": "GPSLongitude"},
    "MeteringMode": {"ExifTool": "MeteringMode"},
    "Genre": {"ExifTool": "Keywords"},
    "SceneCaptureType": {"ExifTool": "SceneCaptureType"},
    "ShutterSpeedValue": {"ExifTool": "ShutterSpeedValue"},
    "Software": {"ExifTool": ["Software", "XMP-tiff:Software"]},
    "FileSource": {"ExifTool": "FileSource"},
    "Title": {"ExifTool": "XMP-dc:Title"},
    "Keywords": {"ExifTool": ["Keywords", "XMP-dc:Subject"]},
    "Location": {"ExifTool": ["GPSLatitude", "GPSLongitude"]},
    "PersonTags": {"ExifTool": "XMP-mwg-rs:RegionName"},
    "CameraMake": {"ExifTool": "XMP-tiff:Make"},
    "CameraModel": {"ExifTool": "XMP-tiff:Model"},
    "Orientation": {"ExifTool": "XMP-tiff:Orientation"}
}

# Path to the input CSV file
csv_file_path = 'ightml.csv'

# Set locale to UTF-8
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


# Function to build the ExifTool command
def build_exiftool_command(row):
    commands = ["-charset", "utf8", "-overwrite_original"]  # Add UTF-8 charset and overwrite flag
    file_path = row.get("FilePath")
    if not file_path or not os.path.exists(file_path):
        print(f"Skipping invalid file path: {file_path}")
        return None

    for column, value in row.items():
        if column in metadata_mapping and value:
            exif_tags = metadata_mapping[column].get("ExifTool")
            if not exif_tags:
                continue
            if isinstance(exif_tags, list):
                for tag in exif_tags:
                    commands.append(f"-{tag}={value}")
            else:
                commands.append(f"-{exif_tags}={value}")

    # Combine commands and add file path
    if commands:
        return ["exiftool"] + commands + [file_path]
    return None


# Process the CSV and apply metadata
def apply_metadata(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            command = build_exiftool_command(row)
            if command:
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"Metadata applied successfully to {row.get('FilePath')}")
                    else:
                        print(f"Error applying metadata to {row.get('FilePath')}: {result.stderr}")
                except Exception as e:
                    print(f"Failed to execute command for {row.get('FilePath')}: {e}")


# Run the script
if __name__ == "__main__":
    apply_metadata(csv_file_path)
