import os
import re
from PIL import Image
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip
from subprocess import run

with open("base_directory.txt", "r") as f:
    base_directory = f.read().strip()

memories_directory = os.path.join(base_directory, "memories")
chat_media_directory = os.path.join(base_directory, "chat_media")
output_directory = os.path.join(base_directory, "snapchat-smddmdwriter")
os.makedirs(output_directory, exist_ok=True)

exif_tags = [
    "AllDates",
    "FileCreateDate",
    "FileModifyDate",
    "QuickTime:CreateDate",
    "QuickTime:ModifyDate",
]
title_tags = ["Title", "Description", "XPTitle"]


def get_file_type(filename):
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    if ext in ['.jpg', '.jpeg', '.png']:
        return 'image'
    elif ext in ['.mp4', '.mov']:
        return 'video'
    return None


def convert_to_valid_riff(file_path):
    try:
        with Image.open(file_path) as img:
            valid_path = file_path + "_converted.png"
            img.save(valid_path, format="PNG")
        os.rename(valid_path, file_path)
        print(f"Converted {file_path} to a valid PNG.")
    except Exception as e:
        print(f"Failed to convert {file_path} to valid PNG: {e}")


def set_exif_tags(file_path, date):
    formatted_date = f"{date} 00:00:00"
    exif_args = []
    for tag in exif_tags:
        exif_args.extend([f"-{tag}={formatted_date}"])
    for tag in title_tags:
        exif_args.extend([f"-{tag}=Snapchat"])
    exif_args.append(file_path)

    try:
        run(["exiftool", *exif_args], check=True)
        backup_file = f"{file_path}_original"
        if os.path.exists(backup_file):
            os.remove(backup_file)
    except Exception as e:
        if "RIFF" in str(e):
            print(f"Retrying after converting RIFF to valid PNG for: {file_path}")
            convert_to_valid_riff(file_path)
            set_exif_tags(file_path, date)
        else:
            print(f"Failed to set EXIF tags for {file_path}: {e}")


def process_main_and_overlay(main_file, overlay_file, output_path):
    main_type = get_file_type(main_file)
    overlay_type = get_file_type(overlay_file)

    if main_type == "image" and overlay_type == "image":
        base_image = Image.open(main_file)
        overlay_image = Image.open(overlay_file).resize(base_image.size, Image.ANTIALIAS)
        combined_image = Image.alpha_composite(
            base_image.convert("RGBA"), overlay_image.convert("RGBA")
        )
        output_path += ".png"
        combined_image.save(output_path)

    elif main_type == "image" and overlay_type == "video":
        base_image = ImageClip(main_file)
        overlay_video = VideoFileClip(overlay_file).resize(base_image.size)
        base_image = base_image.set_duration(overlay_video.duration)
        final_video = CompositeVideoClip([base_image, overlay_video.set_position("center")])
        output_path += ".mp4"
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    elif main_type == "video" and overlay_type == "image":
        main_video = VideoFileClip(main_file)
        overlay_image = ImageClip(overlay_file).set_duration(main_video.duration).resize(main_video.size)
        final_video = CompositeVideoClip([main_video, overlay_image.set_position("center")])
        output_path += ".mp4"
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    elif main_type == "video" and overlay_type == "video":
        main_video = VideoFileClip(main_file)
        overlay_video = VideoFileClip(overlay_file).resize(main_video.size)
        final_video = CompositeVideoClip([main_video, overlay_video.set_position("center")])
        output_path += ".mp4"
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    else:
        raise ValueError("Unsupported combination of file types.")


def process_files(directory):
    file_groups = {}
    for file in os.listdir(directory):
        match = re.match(r"^(.*?)-(main|overlay)\..+$", file)
        if match:
            prefix, suffix = match.groups()
            file_groups.setdefault(prefix, {})[suffix] = os.path.join(directory, file)

    for file in os.listdir(directory):
        date_match = re.match(r"^(\d{4}-\d{2}-\d{2})_", file)
        if not date_match:
            continue
        date = date_match.group(1)
        file_path = os.path.join(directory, file)
        try:
            set_exif_tags(file_path, date)
        except Exception as e:
            print(f"Failed to set EXIF tags for {file}: {e}")

    for prefix, files in file_groups.items():
        main_file = files.get("main")
        overlay_file = files.get("overlay")
        output_path = os.path.join(output_directory, f"{prefix}_processed")

        try:
            if main_file and overlay_file:
                process_main_and_overlay(main_file, overlay_file, output_path)
                print(f"Processed {prefix}: Saved to {output_path}")
            elif main_file:
                main_type = get_file_type(main_file)
                if main_type == "image":
                    base_image = Image.open(main_file)
                    output_path += ".png"
                    base_image.save(output_path)
                elif main_type == "video":
                    main_video = VideoFileClip(main_file)
                    output_path += ".mp4"
                    main_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
                print(f"Processed {prefix} (Main only): Saved to {output_path}")
            else:
                print(f"Skipped {prefix}: No valid files found")
        except Exception as e:
            print(f"Failed {prefix}: {e}")


if __name__ == "__main__":
    process_files(memories_directory)
    process_files(chat_media_directory)
