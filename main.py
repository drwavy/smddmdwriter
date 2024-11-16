import os
import sys
import json
import shutil
import subprocess
import pandas as pd
import csv
from datetime import datetime


# Reads JSON file from provided file path, returns data
def read_json(file_path):
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return None

    with open(file_path, 'r') as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None


# Processes given data (expects dictionary)
def process_data(data):
    if not isinstance(data, dict):
        print("Error: Provided data is not a dictionary.")
        return

    # Example processing: print each key-value pair
    for key, value in data.items():
        print(f"{key}: {value}")


# Function to convert JSON to CSV
def json_to_csv(json_filepath, csv_filepath, fieldnames):
    try:
        # Read JSON data from file
        with open(json_filepath, 'r') as json_file:
            data = json.load(json_file)

        # Write CSV data to file
        with open(csv_filepath, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()

            # Loop through JSON data and write each row to CSV
            for item in data:
                csv_writer.writerow({field: item.get(field, '') for field in fieldnames})

        print(f"Converted {json_filepath} to {csv_filepath}")
    except Exception as e:
        print(f"Error converting JSON to CSV: {e}")


# Function to create CSV folder if it doesn't exist
def create_csv_folder():
    csv_folder_path = os.path.join(os.getcwd(), 'csv')
    if not os.path.exists(csv_folder_path):
        os.makedirs(csv_folder_path)
        print(f"Created CSV folder at {csv_folder_path}")
    return csv_folder_path


# Main function to copy JSON files, convert them to CSV, update CSV paths.
def main():
    # Ask user for target directory path
    target_directory = input("Enter the target directory path: ")

    # Define the source and destination paths
    source_path = os.path.join(target_directory, 'your_instagram_activity', 'content')
    destination_path = os.path.join(os.getcwd(), 'json')

    # List of JSON files to be copied
    json_files = [
        'archived_posts.json', 'igtv_videos.json', 'other_content.json',
        'posts_1.json', 'profile_photos.json', 'reels.json', 'stories.json'
    ]

    # Check if the source directory exists
    if not os.path.exists(source_path):
        print(f"Source directory not found: {source_path}")
        return

    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    # Copy the JSON files
    for file_name in json_files:
        source_file = os.path.join(source_path, file_name)
        destination_file = os.path.join(destination_path, file_name)

        if os.path.exists(source_file):
            shutil.copy2(source_file, destination_file)
            print(f"Copied {file_name} to {destination_path}")
        else:
            print(f"File not found: {file_name}")

    # Create CSV folder
    csv_folder_path = create_csv_folder()

    # Run json2csv_posts_1.py
    json_scripts = [
        'json2csv_profile_photos.py',
        'json2csv_igtv_videos.py',
        'json2csv_reels.py',
        'json2csv_other_content.py',
        'json2csv_stories.py',
        'json2csv_posts_1.py'
    ]

    for script in json_scripts:
        try:
            subprocess.run(['python', script], check=True)
            print(f"{script} executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running {script}: {e}")
            return

    # Update media_uri or uri column in all CSV files in the csv folder
    if os.path.exists(csv_folder_path):
        for csv_file in os.listdir(csv_folder_path):
            if csv_file.endswith('.csv'):
                csv_path = os.path.join(csv_folder_path, csv_file)
                df = pd.read_csv(csv_path)
                if 'media_uri' in df.columns:
                    df['media_uri'] = df['media_uri'].apply(
                        lambda x: os.path.join(target_directory, str(x)) if pd.notna(x) else x)
                    df.to_csv(csv_path, index=False)
                    print(f"Updated media_uri paths in {csv_file}.")
                elif 'uri' in df.columns:
                    df['uri'] = df['uri'].apply(lambda x: os.path.join(target_directory, str(x)) if pd.notna(x) else x)
                    df.to_csv(csv_path, index=False)
                    print(f"Updated uri paths in {csv_file}.")
                else:
                    print(f"No media_uri or uri column found in {csv_file}.")
    else:
        print(f"CSV folder not found at {csv_folder_path}")

    # Run apply_content.py on all CSV files in the csv folder
    if os.path.exists(csv_folder_path):
        for csv_file in os.listdir(csv_folder_path):
            if csv_file.endswith('.csv'):
                try:
                    subprocess.run(['python', 'apply_content.py', csv_file], check=True)
                    print(f"apply_content.py executed successfully on {csv_file}.")
                except subprocess.CalledProcessError as e:
                    print(f"Error running apply_content.py on {csv_file}: {e}")


if __name__ == "__main__":
    main()
