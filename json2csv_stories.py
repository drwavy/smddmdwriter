import json
import csv
from datetime import datetime


def process_stories(json_file, output_csv='csv/stories.csv'):
    with open(json_file, 'r') as f:
        data = json.load(f).get('ig_stories', [])

    fieldnames = [
        'uri', 'creation_timestamp', 'device_id', 'camera_position', 'source_type',
        'title', 'source_app', 'scene_capture_type', 'date_time_original',
        'software', 'iso', 'focal_length', 'lens_model', 'lens_make', 'aperture',
        'shutter_speed', 'metering_mode', 'scene_type', 'music_genre'
    ]

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for story in data:
            uri = story.get('uri', '')
            creation_timestamp = story.get('creation_timestamp', '')
            formatted_timestamp = datetime.fromtimestamp(int(creation_timestamp)).strftime(
                '%Y:%m:%d %H:%M:%S') if creation_timestamp else ''

            device_id = camera_position = source_type = scene_capture_type = date_time_original = software = ''
            iso = focal_length = lens_model = lens_make = aperture = shutter_speed = metering_mode = scene_type = music_genre = ''

            media_metadata = story.get('media_metadata', {})
            exif_data = media_metadata.get('photo_metadata', {}).get('exif_data', []) or media_metadata.get(
                'video_metadata', {}).get('exif_data', [])

            for exif in exif_data:
                if 'device_id' in exif:
                    device_id = exif.get('device_id', '')
                if 'camera_position' in exif:
                    camera_position = exif.get('camera_position', '')
                if 'source_type' in exif:
                    source_type = exif.get('source_type', '')
                if 'scene_capture_type' in exif:
                    scene_capture_type = exif.get('scene_capture_type', '')
                if 'date_time_original' in exif:
                    date_time_original = exif.get('date_time_original', '')
                if 'software' in exif:
                    software = exif.get('software', '')
                if 'iso' in exif:
                    iso = exif.get('iso', '')
                if 'focal_length' in exif:
                    focal_length = exif.get('focal_length', '')
                if 'lens_model' in exif:
                    lens_model = exif.get('lens_model', '')
                if 'lens_make' in exif:
                    lens_make = exif.get('lens_make', '')
                if 'aperture' in exif:
                    aperture = exif.get('aperture', '')
                if 'shutter_speed' in exif:
                    shutter_speed = exif.get('shutter_speed', '')
                if 'metering_mode' in exif:
                    metering_mode = exif.get('metering_mode', '')
                if 'scene_type' in exif:
                    scene_type = exif.get('scene_type', '')

            video_metadata = media_metadata.get('video_metadata', {})
            music_genre = video_metadata.get('music_genre', '')

            title = story.get('title', '')
            post_title = title.encode('latin1').decode('utf-8') if title else ''  # Encoding adjustment
            source_app = story.get('cross_post_source', {}).get('source_app', '')

            writer.writerow({
                'uri': uri,
                'creation_timestamp': formatted_timestamp,
                'device_id': device_id,
                'camera_position': camera_position,
                'source_type': source_type,
                'title': post_title,
                'source_app': source_app,
                'scene_capture_type': scene_capture_type,
                'date_time_original': date_time_original,
                'software': software,
                'iso': iso,
                'focal_length': focal_length,
                'lens_model': lens_model,
                'lens_make': lens_make,
                'aperture': aperture,
                'shutter_speed': shutter_speed,
                'metering_mode': metering_mode,
                'scene_type': scene_type,
                'music_genre': music_genre
            })


json_file_path = 'json/stories.json'

process_stories(json_file_path)

