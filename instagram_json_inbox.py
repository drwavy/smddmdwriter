import pandas as pd
import json
import os
from ftfy import fix_text

with open('base_directory.txt', 'r', encoding='utf-8') as f:
    base_directory = f.read().strip()

inbox_directory = os.path.join(base_directory, 'your_instagram_activity/messages/inbox')

output_csv = 'csv/inbox.csv'

all_records = []

for root, _, files in os.walk(inbox_directory):
    for file in files:
        # if file == 'message_1.json':  # if there's only message_1.json, works for most but doesn't account for edge
        if file.startswith('message_') and file.endswith('.json'):
            json_file_path = os.path.join(root, file)
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                for message in data.get('messages', []):
                    for key in ['photos', 'audio_files', 'videos']:
                        if key in message:
                            for item in message[key]:
                                uri = item.get('uri', '')
                                if uri.startswith('your_instagram_activity/messages/inbox/'):
                                    all_records.append({
                                        'uri': uri,
                                        'creation_timestamp': item.get('creation_timestamp', ''),
                                        'sender_name': fix_text(message.get('sender_name', ''))
                                    })

df = pd.DataFrame(all_records)

df.to_csv(output_csv, index=False)

print(f"Aggregated valid URIs saved to: {output_csv}")
