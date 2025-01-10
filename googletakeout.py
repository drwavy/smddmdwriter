import os
import json
import time
import subprocess


def process_json_files(base_directory):
    for root, _, files in os.walk(base_directory):
        for file in files:
            if file.endswith(".json"):
                json_file_path = os.path.join(root, file)

                with open(json_file_path, "r") as f:
                    data = json.load(f)

                timestamp = data.get("photoTakenTime", {}).get("timestamp")
                if not timestamp:
                    print(f"No timestamp found in {json_file_path}")
                    continue

                date = time.strftime("%Y:%m:%d %H:%M:%S", time.gmtime(int(timestamp)))
                base_name = os.path.splitext(file)[0]
                image_file_path = os.path.join(root, base_name)

                if os.path.isfile(image_file_path):
                    try:
                        subprocess.run([
                            "exiftool",
                            f"-AllDates={date}",
                            f"-FileCreateDate={date}",
                            f"-FileModifyDate={date}",
                            image_file_path
                        ], check=True)

                        backup_file = f"{image_file_path}_original"
                        if os.path.isfile(backup_file):
                            os.remove(backup_file)
                    except subprocess.CalledProcessError as e:
                        print(f"Error processing {image_file_path}: {e}")
                else:
                    print(f"Image file {image_file_path} not found for {json_file_path}")


def main():
    with open("base_directory.txt", "r") as f:
        base_directory = f.read().strip()

    if not os.path.isdir(base_directory):
        print(f"Invalid directory: {base_directory}")
        return

    process_json_files(base_directory)


if __name__ == "__main__":
    main()
