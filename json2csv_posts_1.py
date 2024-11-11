import json
import csv
from datetime import datetime, timezone

# Load JSON data from file
print("Loading JSON data from file...")
with open('json/posts_1.json', 'r') as file:
    data = json.load(file)
print("JSON data loaded successfully.")

# Open CSV file to write
print("Opening CSV file to write...")
with open('csv/posts_1.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header row
    headers = [
        'post_title', 'creation_timestamp',
        'media_uri', 'source_app',
        'latitude', 'longitude', 'device_id',
        'camera_position', 'source_type', 'iso',
        'focal_length', 'lens_model', 'lens_make',
        'aperture', 'shutter_speed', 'software',
        'scene_capture_type', 'scene_type', 'metering_mode'
    ]
    csv_writer.writerow(headers)
    print("Header row written to CSV.")

    # Initialize media item counter
    total_media_items = 0

    # Iterate through each post in the JSON
    for post_index, post in enumerate(data, start=1):
        post_title = post.get('title', '').encode('latin1').decode('utf-8')
        post_creation_timestamp = post.get('creation_timestamp', None)

        # Iterate through each media item in the post
        for media_index, media in enumerate(post.get('media', []), start=1):
            try:
                total_media_items += 1
                media_uri = media.get('uri', '')
                media_creation_timestamp = media.get('creation_timestamp', None)
                media_title = media.get('title', '').encode('latin1').decode('utf-8')
                source_app = media.get('cross_post_source', {}).get('source_app', '')

                print(f"Media Item {total_media_items:05d} | URI        	{media_uri}")
                print(
                    f"Media Item {total_media_items:05d} | TIMESTAMP  	post_creation_timestamp: {post_creation_timestamp if post_creation_timestamp else 'N/A'} / media_creation_timestamp: {media_creation_timestamp if media_creation_timestamp else 'N/A'}")

                # Determine the final creation timestamp (keep the older one)
                if post_creation_timestamp and media_creation_timestamp:
                    if post_creation_timestamp <= media_creation_timestamp:
                        creation_timestamp = post_creation_timestamp
                        chosen_timestamp = "post_creation_timestamp"
                    else:
                        creation_timestamp = media_creation_timestamp
                        chosen_timestamp = "media_creation_timestamp"
                else:
                    creation_timestamp = post_creation_timestamp or media_creation_timestamp
                    chosen_timestamp = "post_creation_timestamp" if post_creation_timestamp else "media_creation_timestamp"

                print(
                    f"Media Item {total_media_items:05d} | TIMESTAMP  	CHOSEN: {chosen_timestamp} VALUE: {creation_timestamp}")

                # Convert UNIX timestamp to EXIFTool format (YYYY:MM:DD HH:MM:SS)
                if creation_timestamp:
                    converted_creation_timestamp = datetime.fromtimestamp(creation_timestamp, timezone.utc).strftime(
                        '%Y:%m:%d %H:%M:%S')
                    print(
                        f"Media Item {total_media_items:05d} | TIMESTAMP  	CONVERTED FROM [ UNIX: {creation_timestamp} ] TO [ {converted_creation_timestamp} ]")
                    creation_timestamp = converted_creation_timestamp
                else:
                    creation_timestamp = 'N/A'
                    print(f"Media Item {total_media_items:05d} | TIMESTAMP  	NO VALID TIMESTAMP AVAILABLE")

                # Determine the final title (prepend media_title if there's a conflict)
                if media_title and post_title:
                    final_title = f"{media_title} - {post_title}"
                    print(
                        f"Media Item {total_media_items:05d} | TITLE      	media_title + post_title: {final_title}")
                else:
                    final_title = post_title or media_title
                    print(f"Media Item {total_media_items:05d} | TITLE      	{final_title}")

                # Extract photo and camera metadata
                media_metadata = media.get('media_metadata', {})
                photo_metadata = media_metadata.get('photo_metadata', {})
                camera_metadata = media_metadata.get('camera_metadata', {})
                exif_data = photo_metadata.get('exif_data', [{}])[0]

                # Extract EXIF information
                latitude = exif_data.get('latitude', '')
                longitude = exif_data.get('longitude', '')
                device_id = exif_data.get('device_id', '')
                camera_position = exif_data.get('camera_position', '')
                source_type = exif_data.get('source_type', '')
                iso = exif_data.get('iso', '')
                focal_length = exif_data.get('focal_length', '')
                lens_model = exif_data.get('lens_model', '')
                lens_make = exif_data.get('lens_make', '')
                aperture = exif_data.get('aperture', '')
                shutter_speed = exif_data.get('shutter_speed', '')
                software = exif_data.get('software', '')
                scene_capture_type = exif_data.get('scene_capture_type', '')
                scene_type = exif_data.get('scene_type', '')
                metering_mode = exif_data.get('metering_mode', '')

                # Log extraction process
                print(f"Media Item {total_media_items:05d} | EXTRACT    	Extracting photo and camera metadata...")

                # Write the row to CSV
                csv_writer.writerow([
                    final_title, creation_timestamp,
                    media_uri, source_app,
                    latitude, longitude, device_id,
                    camera_position, source_type, iso,
                    focal_length, lens_model, lens_make,
                    aperture, shutter_speed, software,
                    scene_capture_type, scene_type, metering_mode
                ])
                print(f"Media Item {total_media_items:05d} | WRITING    	Row written to CSV.")

            except Exception as e:
                print(f"Error processing media item {total_media_items:05d} | URI: {media_uri} | ERROR: {e}")

print(f"Conversion complete. {total_media_items} media items processed. CSV saved as 'csv/posts_1.csv'.")
