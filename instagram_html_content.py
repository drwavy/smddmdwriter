import os
import traceback
import pandas as pd
from bs4 import BeautifulSoup
from ftfy import fix_text
from datetime import datetime

def get_base_directory():
    try:
        with open('base_directory.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError("base_directory.txt not found. Please provide the file.")

def format_timestamp(timestamp):
    try:
        dt = datetime.strptime(timestamp, "%b %d, %Y, %I:%M %p")
        return dt.strftime("%Y:%m:%d %H:%M:%S")
    except ValueError:
        print(f"Warning: Invalid timestamp format: {timestamp}")
        return None

def get_instagram_html_latitude_longitude(content_div):
    latitude, longitude = None, None
    latitude_div = content_div.find("div", string="Latitude")
    if latitude_div:
        latitude_value_div = latitude_div.find_next("div", class_="_a6-q")
        latitude = fix_text(latitude_value_div.text.strip()) if latitude_value_div else None
        if latitude in ["0", "0.0"]:
            latitude = None

    longitude_div = content_div.find("div", string="Longitude")
    if longitude_div:
        longitude_value_div = longitude_div.find_next("div", class_="_a6-q")
        longitude = fix_text(longitude_value_div.text.strip()) if longitude_value_div else None
        if longitude in ["0", "0.0"]:
            longitude = None

    return latitude, longitude

def get_instagram_html_tagged_users(content_div):
    tagged_users_div = content_div.find("div", string="Tagged users")
    if tagged_users_div:
        tagged_users_value_div = tagged_users_div.find_next("div", class_="_a6-q")
        if tagged_users_value_div:
            tagged_users_text = fix_text(tagged_users_value_div.text.strip())
            tagged_users = [
                user.split(" (")[0].strip()
                for user in tagged_users_text.split(",")
                if user.strip() and " (" in user
            ]
            return ", ".join(tagged_users) if tagged_users else ""
    return ""

def parse_archived_posts(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    posts = []
    for post_div in soup.find_all("div", class_="pam _3-95 _2ph- _a6-g uiBoxWhite noborder"):
        title_div = post_div.find("div", class_="_3-95 _2pim _a6-h _a6-i")
        title = fix_text(title_div.text.strip()) if title_div else ""

        media_links = post_div.find_all("a", href=True)

        creation_timestamp_div = post_div.find("div", class_="_3-94 _a6-o")
        creation_timestamp = fix_text(creation_timestamp_div.text.strip()) if creation_timestamp_div else "No Timestamp"
        creation_timestamp = format_timestamp(creation_timestamp)

        latitude, longitude = get_instagram_html_latitude_longitude(post_div)

        tagged_users = get_instagram_html_tagged_users(post_div)

        for media_link in media_links:
            uri = fix_text(media_link['href'])
            posts.append((uri, creation_timestamp, title, latitude, longitude, tagged_users))

    return posts

def parse_other_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    posts = []
    for content_div in soup.find_all("div", class_="pam _3-95 _2ph- _a6-g uiBoxWhite noborder"):
        link = content_div.find("a", href=True)
        uri = fix_text(link['href']) if link else "No URI"

        timestamp_div = content_div.find("div", class_="_3-94 _a6-o")
        creation_timestamp = fix_text(timestamp_div.text.strip()) if timestamp_div else "No Timestamp"
        creation_timestamp = format_timestamp(creation_timestamp)

        title_div = content_div.find("div", class_="_3-95 _2pim _a6-h _a6-i")
        title = fix_text(title_div.text.strip()) if title_div else ""

        latitude, longitude = get_instagram_html_latitude_longitude(content_div)

        tagged_users = get_instagram_html_tagged_users(content_div)

        posts.append((uri, creation_timestamp, title, latitude, longitude, tagged_users))

    return posts

def parse_profile_photos(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    photos = []
    for photo_div in soup.find_all("div", class_="pam _3-95 _2ph- _a6-g uiBoxWhite noborder"):
        link = photo_div.find("a", href=True)
        uri = fix_text(link['href']) if link else "No URI"

        timestamp_div = photo_div.find("div", class_="_3-94 _a6-o")
        creation_timestamp = fix_text(timestamp_div.text.strip()) if timestamp_div else "No Timestamp"
        creation_timestamp = format_timestamp(creation_timestamp)

        title_div = photo_div.find("div", class_="_3-95 _2pim _a6-h _a6-i")
        title = fix_text(title_div.text.strip()) if title_div else "Profile Photo"

        latitude, longitude = get_instagram_html_latitude_longitude(photo_div)

        tagged_users = get_instagram_html_tagged_users(photo_div)

        photos.append((uri, creation_timestamp, title, latitude, longitude, tagged_users))

    return photos

def parse_posts_1(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    posts = []
    for post_div in soup.find_all("div", class_="pam _3-95 _2ph- _a6-g uiBoxWhite noborder"):
        title_div = post_div.find("div", class_="_3-95 _2pim _a6-h _a6-i")
        title = fix_text(title_div.text.strip()) if title_div else ""

        media_links = post_div.find_all("a", href=True)

        timestamp_div = post_div.find("div", class_="_3-94 _a6-o")
        creation_timestamp = fix_text(timestamp_div.text.strip()) if timestamp_div else "No Timestamp"
        creation_timestamp = format_timestamp(creation_timestamp)

        latitude, longitude = get_instagram_html_latitude_longitude(post_div)

        tagged_users = get_instagram_html_tagged_users(post_div)

        for media_link in media_links:
            uri = fix_text(media_link['href'])
            posts.append((uri, creation_timestamp, title, latitude, longitude, tagged_users))

    return posts

def parse_recently_deleted_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    deleted_content = []
    for content_div in soup.find_all("div", class_="pam _3-95 _2ph- _a6-g uiBoxWhite noborder"):
        link = content_div.find("a", href=True)
        uri = fix_text(link['href']) if link else "No URI"

        timestamp_div = content_div.find("div", class_="_3-94 _a6-o")
        creation_timestamp = fix_text(timestamp_div.text.strip()) if timestamp_div else "No Timestamp"
        creation_timestamp = format_timestamp(creation_timestamp)

        title_div = content_div.find("div", class_="_3-95 _2pim _a6-h _a6-i")
        title = fix_text(title_div.text.strip()) if title_div else ""

        latitude, longitude = get_instagram_html_latitude_longitude(content_div)

        tagged_users = get_instagram_html_tagged_users(content_div)

        deleted_content.append((uri, creation_timestamp, title, latitude, longitude,tagged_users))

    return deleted_content

def parse_stories(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    stories = []
    for story_div in soup.find_all("div", class_="pam _3-95 _2ph- _a6-g uiBoxWhite noborder"):
        title_div = story_div.find("div", class_="_3-95 _2pim _a6-h _a6-i")
        title = fix_text(title_div.text.strip()) if title_div else ""

        media_link = story_div.find("a", href=True)
        uri = fix_text(media_link['href']) if media_link else "No URI"

        timestamp_div = story_div.find("div", class_="_3-94 _a6-o")
        creation_timestamp = fix_text(timestamp_div.text.strip()) if timestamp_div else "No Timestamp"
        creation_timestamp = format_timestamp(creation_timestamp)

        latitude = None
        longitude = None
        latitude_div = story_div.find("div", string="Latitude")
        if latitude_div:
            latitude_value_div = latitude_div.find_next("div", class_="_a6-q")
            latitude = fix_text(latitude_value_div.text.strip()) if latitude_value_div else None
            if latitude == "0" or latitude == "0.0":
                latitude = None

        longitude_div = story_div.find("div", string="Longitude")
        if longitude_div:
            longitude_value_div = longitude_div.find_next("div", class_="_a6-q")
            longitude = fix_text(longitude_value_div.text.strip()) if longitude_value_div else None
            if longitude == "0" or longitude == "0.0":
                longitude = None

        tagged_users = get_instagram_html_tagged_users(story_div)


        stories.append((uri, creation_timestamp, title, latitude, longitude, tagged_users))

    return stories

def parse_igtv_videos(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    videos = []
    for video_div in soup.find_all("div", class_="pam _3-95 _2ph- _a6-g uiBoxWhite noborder"):
        title_div = video_div.find("div", class_="_3-95 _2pim _a6-h _a6-i")
        title = fix_text(title_div.text.strip()) if title_div else "No Title"

        media_link = video_div.find("a", href=True)
        uri = fix_text(media_link['href']) if media_link else "No URI"

        timestamp_div = video_div.find("div", class_="_3-94 _a6-o")
        creation_timestamp = fix_text(timestamp_div.text.strip()) if timestamp_div else "No Timestamp"
        creation_timestamp = format_timestamp(creation_timestamp)

        latitude, longitude = get_instagram_html_latitude_longitude(video_div)

        tagged_users = get_instagram_html_tagged_users(video_div)

        videos.append((uri, creation_timestamp, title, latitude, longitude, tagged_users))

    return videos


def process_files(base_directory, output_file="csv/content.csv"):
    content_dir = os.path.join(base_directory, 'content')
    if not os.path.exists(content_dir):
        raise FileNotFoundError(f"Content directory not found: {content_dir}")

    parsers = {
        "archived_posts.html": parse_archived_posts,
        "other_content.html": parse_other_content,
        "profile_photos.html": parse_profile_photos,
        "posts_1.html": parse_posts_1,
        "recently_deleted_content.html": parse_recently_deleted_content,
        "stories.html": parse_stories,
        "igtv_videos.html": parse_igtv_videos,
    }

    data = []
    for file_name in os.listdir(content_dir):
        file_path = os.path.join(content_dir, file_name)
        if os.path.isfile(file_path) and file_name in parsers:
            parser = parsers[file_name]
            try:
                parsed_data = parser(file_path)
                if isinstance(parsed_data, list):
                    data.extend(parsed_data)
                else:
                    data.append(parsed_data)
                print(f"Successfully parsed: {file_name}")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
                print(traceback.format_exc())

    if not data:
        print("No data found to process.")
        return

    expected_columns = ['uri', 'creation_timestamp', 'title', 'Latitude', 'Longitude', 'tagged_users']
    df = pd.DataFrame(data, columns=expected_columns)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"Data successfully saved to: {output_file}")

if __name__ == "__main__":
    try:
        base_directory = get_base_directory()
        process_files(base_directory)
    except Exception as e:
        print(f"An error occurred: {e}")
