import json
import csv
import os
from datetime import datetime


def process_profile_photos(json_file, output_csv='csv/profile_photos.csv'):
    with open(json_file, 'r') as f:
        data = json.load(f).get('ig_profile_picture', [])

    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = [
            'post_title', 'creation_timestamp', 'media_uri', 'source_app', 'latitude', 'longitude', 'device_id',
            'camera_position', 'source_type', 'iso', 'focal_length', 'lens_model', 'lens_make', 'aperture',
            'shutter_speed', 'software', 'scene_capture_type', 'scene_type', 'metering_mode'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for record in data:
            uri = record.get('uri', '')
            creation_timestamp = record.get('creation_timestamp', '')

            if creation_timestamp:
                try:
                    formatted_timestamp = datetime.fromtimestamp(int(creation_timestamp)).strftime('%Y:%m:%d %H:%M:%S')
                except ValueError:
                    formatted_timestamp = ''
            else:
                formatted_timestamp = ''

            title = record.get('title', '')
            source_app = record.get('cross_post_source', {}).get('source_app', '')

            latitude = ''
            longitude = ''
            device_id = ''
            camera_position = ''
            source_type = ''
            iso = ''
            focal_length = ''
            lens_model = ''
            lens_make = ''
            aperture = ''
            shutter_speed = ''
            software = ''
            scene_capture_type = ''
            scene_type = ''
            metering_mode = ''

            writer.writerow({
                'post_title': title,
                'creation_timestamp': formatted_timestamp,
                'media_uri': uri,
                'source_app': source_app,
                'latitude': latitude,
                'longitude': longitude,
                'device_id': device_id,
                'camera_position': camera_position,
                'source_type': source_type,
                'iso': iso,
                'focal_length': focal_length,
                'lens_model': lens_model,
                'lens_make': lens_make,
                'aperture': aperture,
                'shutter_speed': shutter_speed,
                'software': software,
                'scene_capture_type': scene_capture_type,
                'scene_type': scene_type,
                'metering_mode': metering_mode
            })

            print(f"URI: {uri}, Creation Timestamp: {formatted_timestamp}, Title: {title}, Source App: {source_app}")


json_file_path = 'json/profile_photos.json'

process_profile_photos(json_file_path)

