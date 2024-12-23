import os
import pandas as pd
import json
from ftfy import fix_text

def get_base_directory():
    with open("base_directory.txt", "r") as file:
        return file.read().strip()

def parse_json_file(file_path, rows, key_mapping=None):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}. Skipping...")
        return

    with open(file_path, "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            print(f"Invalid JSON in {file_path}. Skipping...")
            return

    if key_mapping:
        for item in data:
            media_items = item.get("media", [])
            for media in media_items:
                uri = media.get("uri", "")
                creation_timestamp = media.get("creation_timestamp", "")
                latitude, longitude = None, None
                title = fix_text(media.get("title", ""))

                exif_data = (
                    media.get("media_metadata", {})
                    .get("photo_metadata", {})
                    .get("exif_data", [])
                )
                if isinstance(exif_data, list):
                    for exif in exif_data:
                        latitude = exif.get("latitude", latitude)
                        longitude = exif.get("longitude", longitude)

                rows.append({
                    "uri": uri,
                    "creation_timestamp": creation_timestamp,
                    "latitude": latitude,
                    "longitude": longitude,
                    "title": title
                })
    else:
        for section_key, content_key in [
            ("ig_archived_post_media", "media"),
            ("ig_igtv_media", "media"),
            ("ig_other_media", "media"),
            ("media", None),
            ("ig_profile_picture", None),
            ("ig_reels_media", "media"),
            ("ig_stories", None)
        ]:
            if section_key in data:
                for item in data[section_key]:
                    media_items = item[content_key] if content_key else [item]
                    for media in media_items:
                        uri = media.get("uri", "")
                        creation_timestamp = media.get("creation_timestamp", "")
                        latitude, longitude = None, None
                        title = fix_text(media.get("title", ""))

                        exif_data = (
                            media.get("media_metadata", {})
                            .get("photo_metadata", {})
                            .get("exif_data", [])
                        )
                        if isinstance(exif_data, list):
                            for exif in exif_data:
                                latitude = exif.get("latitude", latitude)
                                longitude = exif.get("longitude", longitude)

                        rows.append({
                            "uri": uri,
                            "creation_timestamp": creation_timestamp,
                            "latitude": latitude,
                            "longitude": longitude,
                            "title": title
                        })

def process_all_files(base_path, output_csv):
    rows = []

    parse_json_file(os.path.join(base_path, "archived_posts.json"), rows)
    parse_json_file(os.path.join(base_path, "igtv_videos.json"), rows)
    parse_json_file(os.path.join(base_path, "other_content.json"), rows)
    parse_json_file(os.path.join(base_path, "posts_1.json"), rows, key_mapping=True)
    parse_json_file(os.path.join(base_path, "profile_photos.json"), rows)
    parse_json_file(os.path.join(base_path, "reels.json"), rows)
    parse_json_file(os.path.join(base_path, "stories.json"), rows)

    df = pd.DataFrame(rows)

    df = df[~df['uri'].str.startswith("https://", na=False)]

    if df.empty:
        print("No data found in any files. Skipping...")
    else:
        df.to_csv(output_csv, index=False, header=["uri", "creation_timestamp", "latitude", "longitude", "title"])

if __name__ == "__main__":
    base_directory = get_base_directory()
    content_path = os.path.join(base_directory, "your_instagram_activity", "content")

    process_all_files(content_path, "csv/content.csv")
