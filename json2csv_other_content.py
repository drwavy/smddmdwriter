import json
import csv
import os
from datetime import datetime, timezone


def process_other_content(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    records = []
    for entry in data.get('ig_other_media', []):
        for media in entry.get('media', []):
            record = {
                'post_title': media.get('title', '').strip() if media.get('title') else None,
                'creation_timestamp': convert_timestamp(media.get('creation_timestamp', '')),
                'media_uri': media.get('uri', ''),
                'source_app': media.get('cross_post_source', {}).get('source_app', 'Unknown'),
                'latitude': get_nested_value(media, ['media_metadata', 'photo_metadata', 'exif_data', 0, 'latitude']),
                'longitude': get_nested_value(media, ['media_metadata', 'photo_metadata', 'exif_data', 0, 'longitude']),
                'device_id': get_nested_value(media, ['media_metadata', 'photo_metadata', 'exif_data', 0, 'device_id']),
                'camera_position': get_nested_value(media, ['media_metadata', 'photo_metadata', 'exif_data', 0,
                                                            'camera_position']),
                'source_type': get_nested_value(media,
                                                ['media_metadata', 'photo_metadata', 'exif_data', 0, 'source_type']),
                'iso': get_nested_value(media, ['media_metadata', 'photo_metadata', 'exif_data', 0, 'iso']),
                'focal_length': get_nested_value(media,
                                                 ['media_metadata', 'photo_metadata', 'exif_data', 0, 'focal_length']),
                'lens_model': get_nested_value(media,
                                               ['media_metadata', 'photo_metadata', 'exif_data', 0, 'lens_model']),
                'lens_make': get_nested_value(media, ['media_metadata', 'photo_metadata', 'exif_data', 0, 'lens_make']),
                'aperture': get_nested_value(media, ['media_metadata', 'photo_metadata', 'exif_data', 0, 'aperture']),
                'shutter_speed': get_nested_value(media, ['media_metadata', 'photo_metadata', 'exif_data', 0,
                                                          'shutter_speed']),
                'software': get_nested_value(media, ['media_metadata', 'photo_metadata', 'exif_data', 0, 'software']),
                'scene_capture_type': get_nested_value(media, ['media_metadata', 'photo_metadata', 'exif_data', 0,
                                                               'scene_capture_type']),
                'scene_type': get_nested_value(media,
                                               ['media_metadata', 'photo_metadata', 'exif_data', 0, 'scene_type']),
                'metering_mode': get_nested_value(media,
                                                  ['media_metadata', 'photo_metadata', 'exif_data', 0, 'metering_mode'])
            }
            records.append(record)
    return records


def get_nested_value(data, keys):
    try:
        for key in keys:
            if isinstance(data, list) and isinstance(key, int):
                data = data[key]
            elif isinstance(data, dict):
                data = data.get(key, {})
            else:
                return None
        return data if data != {} else None
    except (IndexError, AttributeError, TypeError):
        return None


def convert_timestamp(timestamp):
    try:
        return datetime.fromtimestamp(int(timestamp), tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return 'Invalid Timestamp'


def write_csv(records, output_file):
    keys = ['post_title', 'creation_timestamp', 'media_uri', 'source_app', 'latitude', 'longitude', 'device_id',
            'camera_position', 'source_type', 'iso', 'focal_length', 'lens_model', 'lens_make', 'aperture',
            'shutter_speed', 'software', 'scene_capture_type', 'scene_type', 'metering_mode']
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(records)


def ensure_directory_exists(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


if __name__ == "__main__":
    json_file_path = 'json/other_content.json'
    output_csv_path = 'csv/other_content.csv'

    ensure_directory_exists(output_csv_path)
    other_content_records = process_other_content(json_file_path)
    write_csv(other_content_records, output_csv_path)
