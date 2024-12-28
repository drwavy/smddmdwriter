import os
import csv
from bs4 import BeautifulSoup
from datetime import datetime
from ftfy import fix_text

base_directory_file = "base_directory.txt"

with open(base_directory_file, "r", encoding="utf-8") as file:
    base_directory = file.read().strip()

inbox_directory = os.path.join(base_directory, "messages", "inbox")

output_csv = "csv/inbox.csv"

os.makedirs(os.path.dirname(output_csv), exist_ok=True)

with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["src", "sender_name", "creation_timestamp"])

    for root, dirs, files in os.walk(inbox_directory):
        for file in files:
            if file == "message_1.html":
                file_path = os.path.join(root, file)

                with open(file_path, "r", encoding="utf-8") as html_file:
                    soup = BeautifulSoup(html_file, "html.parser")

                messages = soup.find_all("div", class_="pam _3-95 _2ph- _a6-g uiBoxWhite noborder")

                for message in messages:
                    sender_name_div = message.find("div", class_="_3-95 _2pim _a6-h _a6-i")
                    sender_name = fix_text(sender_name_div.text.strip()) if sender_name_div else None

                    media = message.find(["audio", "video", "img"])
                    if media:
                        uri = media.get("src")

                        time_div = message.find("div", class_="_3-94 _a6-o")
                        if time_div:
                            raw_time = time_div.text.strip()
                            try:
                                creation_timestamp = datetime.strptime(raw_time, "%b %d, %Y, %I:%M %p").strftime("%Y:%m:%d %H:%M:%S")
                            except ValueError:
                                creation_timestamp = raw_time

                        writer.writerow([uri, sender_name, creation_timestamp])

print(f"Parsing complete. Data has been saved to {output_csv}")
