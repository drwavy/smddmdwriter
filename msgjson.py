import os
import json
import csv
from datetime import datetime


def process_messages(base_directory, output_file='csv/messages_media.csv'):
    if not os.path.exists(base_directory):
        print(f"Error: The base directory '{base_directory}' does not exist.")
        return

    messages_path = os.path.join(base_directory, 'your_instagram_activity', 'messages', 'inbox')
    if not os.path.exists(messages_path):
        print(f"Error: The messages directory '{messages_path}' does not exist.")
        return

    subdirectories = [name for name in os.listdir(messages_path) if os.path.isdir(os.path.join(messages_path, name))]
    print(f"Subdirectories in inbox: {subdirectories}")
    print(f"Number of subdirectories: {len(subdirectories)}")

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['SourceFile', 'AllDates', 'Keyword']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for subdirectory in subdirectories:
            message_file_path = os.path.join(messages_path, subdirectory, 'message_1.json')
            if os.path.exists(message_file_path):
                print(f"Processing {subdirectory}...")

                with open(message_file_path, 'r', encoding='utf-8') as json_file:
                    try:
                        data = json.load(json_file)

                        for message in data.get('messages', []):
                            for media_type in ['photos', 'videos', 'audio_files']:
                                if media_type in message and isinstance(message[media_type], list):
                                    for media in message[media_type]:
                                        if 'uri' in media and 'creation_timestamp' in media:
                                            writer.writerow({
                                                'SourceFile': os.path.join(base_directory, media['uri']),
                                                'AllDates': datetime.utcfromtimestamp(
                                                    media['creation_timestamp']
                                                ).strftime('%Y:%m:%d %H:%M:%S'),
                                                'Keyword': message.get('sender_name', '')
                                            })
                                            print(f"Logged media from {subdirectory}: {media['uri']}")
                    except json.JSONDecodeError:
                        print(f"Error: Could not parse JSON in {message_file_path}")
            else:
                print(f"Warning: {subdirectory} does not contain message_1.json")

    print(f"Media data logged to {output_file}")


if __name__ == "__main__":
    base_directory = input("Enter the base directory containing the Instagram data: ")
    process_messages(base_directory)
