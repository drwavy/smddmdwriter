import json
import csv
from datetime import datetime


def process_archived_posts(json_file, output_csv='csv/archived_posts.csv'):
    # Load JSON data
    with open(json_file, 'r') as f:
        data = json.load(f).get('ig_archived_post_media', [])

    # Define CSV output fields, renaming 'title' to 'post_title' to align with posts_1.csv
    fieldnames = [
        'uri', 'creation_timestamp', 'latitude', 'longitude', 'device_id', 'camera_position',
        'source_type', 'post_title', 'source_app', 'scene_capture_type', 'date_time_original',
        'software', 'iso', 'focal_length', 'lens_model', 'lens_make', 'aperture', 'shutter_speed',
        'metering_mode', 'scene_type', 'subtitles_uri', 'subtitles_creation_timestamp'
    ]

    # Open CSV output file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Process each archived post entry
        for post in data:
            for media in post.get('media', []):
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

                title = media.get('title', '')
                post_title = title.encode('latin1').decode('utf-8') if title else ''  # Encoding to match posts_1

                source_app = media.get('cross_post_source', {}).get('source_app', '')

                # Other metadata fields are initialized or extracted similarly
                # ...

                # Write extracted data to CSV
                writer.writerow({
                    'uri': uri,
                    'creation_timestamp': formatted_timestamp,
                    'post_title': post_title,
                    'source_app': source_app,
                    # other fields go here
                })


# Path to the archived posts JSON file
json_file_path = 'json/archived_posts.json'

# Process the archived posts JSON
process_archived_posts(json_file_path)

