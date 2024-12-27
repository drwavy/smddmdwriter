import os
import pandas as pd
from bs4 import BeautifulSoup
from ftfy import fix_text
from datetime import datetime

def get_base_directory():
    try:
        with open('base_directory.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        raise Exception("base_directory.txt not found")

def format_timestamp(timestamp):
    try:
        dt = datetime.strptime(timestamp, "%b %d, %Y, %I:%M %p")
        return dt.strftime("%Y:%m:%d %H:%M:%S")
    except ValueError:
        return "Invalid Timestamp"

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

        for media_link in media_links:
            uri = fix_text(media_link['href'])
            posts.append((uri, creation_timestamp, title))

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

        title = ""
        posts.append((uri, creation_timestamp, title))

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

        title = "Profile Photos"
        photos.append((uri, creation_timestamp, title))

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

        for media_link in media_links:
            uri = fix_text(media_link['href'])
            posts.append((uri, creation_timestamp, title))

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

        title = ""
        deleted_content.append((uri, creation_timestamp, title))

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

        stories.append((uri, creation_timestamp, title))

    return stories

def process_files(base_directory):
    content_dir = os.path.join(base_directory, 'content')
    if not os.path.exists(content_dir):
        raise Exception(f"Content directory not found: {content_dir}")

    parsers = {
        "archived_posts.html": parse_archived_posts,
        "other_content.html": parse_other_content,
        "profile_photos.html": parse_profile_photos,
        "posts_1.html": parse_posts_1,
        "recently_deleted_content.html": parse_recently_deleted_content,
        "stories.html": parse_stories,
    }

    data = []
    for file_name in os.listdir(content_dir):
        file_path = os.path.join(content_dir, file_name)
        if os.path.isfile(file_path) and file_name in parsers:
            parser = parsers[file_name]
            parsed_data = parser(file_path)
            if isinstance(parsed_data, list):
                data.extend(parsed_data)
            else:
                data.append(parsed_data)

    df = pd.DataFrame(data, columns=['uri', 'creation_timestamp', 'title'])
    output_file = "csv/content.csv"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    base_directory = get_base_directory()
    process_files(base_directory)
