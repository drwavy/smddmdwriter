import os
import subprocess
import pandas as pd

with open('base_directory.txt', 'r', encoding='utf-8') as f:
    base_directory = f.read().strip()

inbox_directory = os.path.join(base_directory, 'your_instagram_activity/messages/inbox')

output_csv = 'csv/inbox.csv'

def convert_file(input_path, output_path, codec=None):
    try:
        command = ["ffmpeg", "-i", input_path, "-map_metadata", "0"]
        if codec:
            command += ["-c:v" if codec == "jpg" else "-c:a", codec]
        command.append(output_path)

        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Converted: {input_path} -> {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_path}: {e}")

def process_files_in_csv():
    if not os.path.exists(output_csv):
        print("CSV file not found!")
        return

    df = pd.read_csv(output_csv)

    for index, row in df.iterrows():
        uri = row.get("uri", "")
        if not uri:
            continue

        full_path = os.path.join(base_directory, uri)

        if "/audio/" in uri:
            if not os.path.splitext(uri)[1]:
                uri += ".mp4"
                os.rename(full_path, full_path + ".mp4")
                full_path += ".mp4"
            if not uri.endswith(".m4a"):
                new_uri = os.path.splitext(uri)[0] + ".m4a"
                new_full_path = os.path.join(base_directory, new_uri)
                convert_file(full_path, new_full_path, codec="aac")
                os.remove(full_path)
                df.at[index, "uri"] = new_uri

        elif "/photos/" in uri:
            if not os.path.splitext(uri)[1]:
                uri += ".jpg"
                os.rename(full_path, full_path + ".jpg")
                full_path += ".jpg"
            if not uri.endswith(".jpg"):
                new_uri = os.path.splitext(uri)[0] + ".jpg"
                new_full_path = os.path.join(base_directory, new_uri)
                convert_file(full_path, new_full_path, codec="mjpeg")
                os.remove(full_path)
                df.at[index, "uri"] = new_uri

        elif "/videos/" in uri:
            if not os.path.splitext(uri)[1]:
                uri += ".mp4"
                os.rename(full_path, full_path + ".mp4")
                full_path += ".mp4"
            if not uri.endswith(".mp4"):
                new_uri = os.path.splitext(uri)[0] + ".mp4"
                new_full_path = os.path.join(base_directory, new_uri)
                convert_file(full_path, new_full_path, codec=None)
                os.remove(full_path)
                df.at[index, "uri"] = new_uri

    df.to_csv(output_csv, index=False)
    print("CSV updated successfully.")

if __name__ == "__main__":
    process_files_in_csv()
