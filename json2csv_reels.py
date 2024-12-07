import json
import csv
from datetime import datetime


def process_reels(json_file, output_csv='csv/reels.csv'):
    with open(json_file, 'r') as f:
        data = json.load(f).get('ig_reels_media', [])

    fieldnames = [
        'uri', 'creation_timestamp', 'latitude', 'longitude', 'device_id', 'camera_position',
        'source_type', 'title', 'source_app', 'subtitles_uri', 'subtitles_creation_timestamp'
    ]

    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for reel in data:
            for media in reel.get('media', []):
                # Basic reel details
                uri = media.get('uri', '')
                creation_timestamp = media.get('creation_timestamp', '')

                if creation_timestamp:
                    try:
                        formatted_timestamp = datetime.fromtimestamp(int(creation_timestamp)).strftime(
                            '%Y:%m:%d %H:%M:%S')
                    except ValueError:
                        formatted_timestamp = ''
                else:
                    formatted_timestamp = ''

                video_metadata = media.get('media_metadata', {}).get('video_metadata', {})
                latitude = ''
                longitude = ''
                device_id = ''
                camera_position = ''
                source_type = ''

                exif_data = video_metadata.get('exif_data', [])
                for exif in exif_data:
                    if 'latitude' in exif:
                        latitude = exif.get('latitude', '')
                    if 'longitude' in exif:
                        longitude = exif.get('longitude', '')
                    if 'device_id' in exif:
                        device_id = exif.get('device_id', '')
                    if 'camera_position' in exif:
                        camera_position = exif.get('camera_position', '')
                    if 'source_type' in exif:
                        source_type = exif.get('source_type', '')

                subtitles = video_metadata.get('subtitles', {})
                subtitles_uri = subtitles.get('uri', '')
                subtitles_creation_timestamp = subtitles.get('creation_timestamp', '')

                if subtitles_creation_timestamp:
                    try:
                        subtitles_creation_timestamp = datetime.fromtimestamp(
                            int(subtitles_creation_timestamp)).strftime('%Y:%m:%d %H:%M:%S')
                    except ValueError:
                        subtitles_creation_timestamp = ''

                title = media.get('title', '')
                source_app = media.get('cross_post_source', {}).get('source_app', '')

                writer.writerow({
                    'uri': uri,
                    'creation_timestamp': formatted_timestamp,
                    'latitude': latitude,
                    'longitude': longitude,
                    'device_id': device_id,
                    'camera_position': camera_position,
                    'source_type': source_type,
                    'title': title,
                    'source_app': source_app,
                    'subtitles_uri': subtitles_uri,
                    'subtitles_creation_timestamp': subtitles_creation_timestamp
                })


json_file_path = 'json/reels.json'

process_reels(json_file_path)

