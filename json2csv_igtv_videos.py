import json
import csv
from datetime import datetime


def process_igtv_videos(json_file, output_csv='csv/igtv_videos.csv'):
    # Load JSON data
    with open(json_file, 'r') as f:
        data = json.load(f).get('ig_igtv_media', [])

    # Define CSV output fields
    fieldnames = [
        'uri', 'creation_timestamp', 'device_id', 'title', 'source_app'
    ]

    # Open CSV output file
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Process each IGTV entry
        for igtv in data:
            for media in igtv.get('media', []):
                # Basic IGTV details
                uri = media.get('uri', '')
                creation_timestamp = media.get('creation_timestamp', '')

                # Convert UNIX timestamp to EXIFTool format (YYYY:MM:DD HH:MM:SS)
                if creation_timestamp:
                    try:
                        formatted_timestamp = datetime.fromtimestamp(int(creation_timestamp)).strftime(
                            '%Y:%m:%d %H:%M:%S')
                    except ValueError:
                        formatted_timestamp = ''
                else:
                    formatted_timestamp = ''

                # Metadata extraction
                video_metadata = media.get('media_metadata', {}).get('video_metadata', {})
                device_id = ''

                # Extract EXIF data if available
                exif_data = video_metadata.get('exif_data', [])
                for exif in exif_data:
                    if 'device_id' in exif:
                        device_id = exif.get('device_id', '')

                # Additional metadata
                title = media.get('title', '')
                source_app = media.get('cross_post_source', {}).get('source_app', '')

                # Write extracted data to CSV
                writer.writerow({
                    'uri': uri,
                    'creation_timestamp': formatted_timestamp,
                    'device_id': device_id,
                    'title': title,
                    'source_app': source_app
                })


# Path to the IGTV videos JSON file
json_file_path = 'json/igtv_videos.json'

# Process the IGTV videos JSON
process_igtv_videos(json_file_path)
