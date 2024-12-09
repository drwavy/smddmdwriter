import os
from bs4 import BeautifulSoup
import pandas as pd

# Prompt the user for the base directory
base_dir = input("Enter the base directory path: ")
inbox_path = os.path.join(base_dir, "messages", "inbox")

# Prepare lists to hold data for CSV
data = {
    "Chat Title": [],
    "Message Sender Name": [],
    "Timestamp": [],
    "Message Content": [],
    "Message Content Media Item Type": [],
    "Message Content Media Item Path": []
}

# Traverse each subfolder in the inbox directory
for subfolder in os.listdir(inbox_path):
    subfolder_path = os.path.join(inbox_path, subfolder)
    if os.path.isdir(subfolder_path):
        message_file_path = os.path.join(subfolder_path, "message_1.html")
        if os.path.exists(message_file_path):
            with open(message_file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')

            # Extract chat title
            chat_title = soup.find('div', class_='_a70e').text if soup.find('div', class_='_a70e') else "Unknown"

            # Parse all messages
            messages = soup.find_all('div', class_='pam _3-95 _2ph- _a6-g uiBoxWhite noborder')
            for message in messages:
                sender_div = message.find('div', class_='_3-95 _2pim _a6-h _a6-i')
                content_div = message.find('div', class_='_3-95 _a6-p')
                timestamp_div = message.find('div', class_='_3-94 _a6-o')

                sender_name = sender_div.text if sender_div else "Unknown"
                timestamp = timestamp_div.text if timestamp_div else "Unknown"

                if content_div:
                    # Extract text content
                    content_text = content_div.text.strip()
                    # Check for media items
                    media = content_div.find(['audio', 'video', 'img'])
                    media_type = media.name if media else "Text"
                    media_path = media.get('src', media.get('href', '')) if media else ""
                else:
                    content_text = ""
                    media_type = "None"
                    media_path = ""

                # Append data
                data["Chat Title"].append(chat_title)
                data["Message Sender Name"].append(sender_name)
                data["Timestamp"].append(timestamp)
                data["Message Content"].append(content_text)
                data["Message Content Media Item Type"].append(media_type)
                data["Message Content Media Item Path"].append(media_path)

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
output_file = 'ightmlmsg.csv'
df.to_csv(output_file, index=False)
print(f"Data extracted and saved to {output_file}")
