import os
import pandas as pd
import subprocess

csv_folder = 'csv'

csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]

def sanitize_value(value, default=""):
    if pd.isna(value) or not isinstance(value, str):
        return default
    return value.strip()

def apply_metadata(row, file_name):
    media_file = sanitize_value(row.get('media_uri') or row.get('uri'))
    if not media_file:
        print(f"Skipping row in {file_name}: No valid media URI found.")
        return

    datetime_original = sanitize_value(row.get('creation_timestamp'))
    metadata = {
        "XMP:Title": sanitize_value(row.get('post_title') or row.get('title')),
        "EXIF:DateTimeOriginal": datetime_original,
        "EXIF:CreateDate": datetime_original,
        "EXIF:ModifyDate": datetime_original,
        "EXIF:GPSLatitude": row.get('latitude', ""),
        "EXIF:GPSLongitude": row.get('longitude', ""),
        "XMP:DeviceID": sanitize_value(row.get('device_id')),
        "XMP:CameraPosition": sanitize_value(row.get('camera_position')),
        "EXIF:ISO": row.get('iso', ""),
        "EXIF:FocalLength": row.get('focal_length', ""),
        "EXIF:LensModel": sanitize_value(row.get('lens_model')),
        "EXIF:LensMake": sanitize_value(row.get('lens_make')),
        "EXIF:ApertureValue": row.get('aperture', ""),
        "EXIF:ShutterSpeedValue": row.get('shutter_speed', ""),
        "XMP:Software": sanitize_value(row.get('software')),
        "XMP:SceneCaptureType": sanitize_value(row.get('scene_capture_type')),
        "XMP:SceneType": row.get('scene_type', ""),
        "EXIF:MeteringMode": row.get('metering_mode', "")
    }

    metadata = {k: v for k, v in metadata.items() if pd.notna(v) and v != ""}

    command = ["exiftool", "-overwrite_original"]
    for key, value in metadata.items():
        command.append(f"-{key}={value}")
    if datetime_original:
        command.extend([f"-FileCreateDate={datetime_original}", f"-FileModifyDate={datetime_original}"])
    command.append(media_file)

    try:
        print(f"Applying metadata to {media_file} from {file_name}")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error applying metadata to {media_file} from {file_name}: {e.stderr}")
    except Exception as e:
        print(f"Unexpected error for {media_file} in {file_name}: {str(e)}")

for csv_file in csv_files:
    file_path = os.path.join(csv_folder, csv_file)
    print(f"\nProcessing file: {csv_file}")
    data = pd.read_csv(file_path)
    for _, row in data.iterrows():
        apply_metadata(row, csv_file)

