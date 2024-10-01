import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

base_folder = input("Please enter the path to the base folder: ")

log_file_path = 'console_output.txt'
log_file = open(log_file_path, 'w')
sys.stdout = log_file
sys.stderr = log_file


def convert_timestamp_to_exif(creation_timestamp):
    return datetime.fromtimestamp(creation_timestamp, tz=timezone.utc).strftime('%Y:%m:%d %H:%M:%S')


def clean_caption(title):
    if title:
        cleaned_title = title.replace('\n', ' ').strip()
        try:
            cleaned_title = cleaned_title.encode('utf-8', 'replace').decode('utf-8')
        except UnicodeEncodeError as e:
            print(f"Error encoding title '{title}': {e}")
            cleaned_title = re.sub(r'[^\x00-\x7F]+', '?', cleaned_title)
        return cleaned_title
    return ''


def apply_metadata_to_file(metadata, file_path):
    command = ['exiftool', '-charset', 'utf8', '-E']

    if 'DateTimeOriginal' in metadata:
        datetime_value = metadata['DateTimeOriginal']
        command += [f'-DateTimeOriginal={datetime_value}', f'-MediaCreateDate={datetime_value}',
                    f'-MediaModifyDate={datetime_value}', f'-CreateDate={datetime_value}',
                    f'-ModifyDate={datetime_value}',
                    f'-FileModifyDate={datetime_value}']
    if 'Caption-Abstract' in metadata and metadata['Caption-Abstract']:
        command += [f'-Caption-Abstract={metadata["Caption-Abstract"]}']
    if 'GPSLatitude' in metadata and 'GPSLongitude' in metadata:
        command += [f'-GPSLatitude={metadata["GPSLatitude"]}', f'-GPSLongitude={metadata["GPSLongitude"]}']

    command += ['-overwrite_original', file_path]
    print(f"Running command: {' '.join(command)}")

    subprocess.run(command)


def map_json_to_media_dir(json_file):
    if 'archived' in json_file:
        return 'archived_posts'
    elif 'posts' in json_file:
        return 'posts'
    elif 'stories' in json_file:
        return 'stories'
    elif 'other' in json_file:
        return 'other'
    return None


def find_media_file(media_base_folder, media_uri):
    exact_path = os.path.join(media_base_folder, media_uri.lstrip('/'))
    if os.path.isfile(exact_path):
        return exact_path

    for root, dirs, files in os.walk(media_base_folder):
        for file in files:
            if file in media_uri:
                return os.path.join(root, file)

    return None


def process_json_file(json_data, media_base_folder, base_folder):
    if isinstance(json_data, dict):
        for key, media_items in json_data.items():
            if isinstance(media_items, list):
                for item in media_items:
                    if isinstance(item, dict):
                        media_uri = item.get('uri', None)
                        if not media_uri:
                            continue

                        if media_uri.startswith('http://') or media_uri.startswith('https://'):
                            print(f"Skipping external URI: {media_uri}")
                            continue

                        media_file_path = find_media_file(media_base_folder, media_uri)

                        if not media_file_path:
                            print(f"Warning: File not found for URI: {media_uri}")
                            continue

                        file_metadata = {}
                        file_metadata['SourceFile'] = media_file_path

                        if media_file_path.endswith(('.mp4', '.mov')):
                            continue
                        else:
                            file_metadata['DateTimeOriginal'] = convert_timestamp_to_exif(item['creation_timestamp'])
                            file_metadata['Caption-Abstract'] = clean_caption(item['title'])

                            photo_metadata = item['media_metadata'].get('photo_metadata', {})
                            exif_data_list = photo_metadata.get('exif_data', [])
                            if exif_data_list:
                                exif_data = exif_data_list[0]
                                if 'latitude' in exif_data:
                                    file_metadata['GPSLatitude'] = exif_data['latitude']
                                if 'longitude' in exif_data:
                                    file_metadata['GPSLongitude'] = exif_data['longitude']

                            apply_metadata_to_file(file_metadata, file_metadata['SourceFile'])
    elif isinstance(json_data, list):
        for item in json_data:
            if isinstance(item, dict):
                media_uri = item.get('uri', None)
                if not media_uri:
                    continue

                if media_uri.startswith('http://') or media_uri.startswith('https://'):
                    print(f"Skipping external URI: {media_uri}")
                    continue

                media_file_path = find_media_file(media_base_folder, media_uri)

                if not media_file_path:
                    print(f"Warning: File not found for URI: {media_uri}")
                    continue

                file_metadata = {}
                file_metadata['SourceFile'] = media_file_path

                if media_file_path.endswith(('.mp4', '.mov')):
                    continue
                else:
                    file_metadata['DateTimeOriginal'] = convert_timestamp_to_exif(item['creation_timestamp'])
                    file_metadata['Caption-Abstract'] = clean_caption(item['title'])

                    photo_metadata = item['media_metadata'].get('photo_metadata', {})
                    exif_data_list = photo_metadata.get('exif_data', [])
                    if exif_data_list:
                        exif_data = exif_data_list[0]
                        if 'latitude' in exif_data:
                            file_metadata['GPSLatitude'] = exif_data['latitude']
                        if 'longitude' in exif_data:
                            file_metadata['GPSLongitude'] = exif_data['longitude']

                    apply_metadata_to_file(file_metadata, file_metadata['SourceFile'])
    else:
        print(f"Unsupported JSON format: {type(json_data)}")


def process_all_json(base_folder):
    content_folder = os.path.join(base_folder, 'your_instagram_activity', 'content')
    media_base_folder = os.path.join(base_folder, 'media')

    for json_file in os.listdir(content_folder):
        if json_file.endswith('.json'):
            json_path = os.path.join(content_folder, json_file)
            media_dir = map_json_to_media_dir(json_file)

            if media_dir:
                print(f"Processing JSON file: {json_file} for media folder: {media_dir}")
                with open(json_path, 'r') as f:
                    json_data = json.load(f)

                media_folder = os.path.join(media_base_folder, media_dir)
                process_json_file(json_data, media_folder, base_folder)


process_all_json(base_folder)
log_file.close()
