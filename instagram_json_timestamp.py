import pandas as pd
import os

folder_path = 'csv'

def convert_timestamp(ts):
    try:
        if len(str(ts)) > 10:
            return pd.to_datetime(int(ts), unit='ms').strftime('%Y:%m:%d %H:%M:%S')
        else:
            return pd.to_datetime(int(ts), unit='s').strftime('%Y:%m:%d %H:%M:%S')
    except Exception as e:
        return None

for file_name in os.listdir(folder_path):
    if file_name.endswith(".csv"):
        file_path = os.path.join(folder_path, file_name)
        print(f"Processing file: {file_name}")

        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            print(f"Error loading file {file_name}: {e}")
            continue

        if 'creation_timestamp' in df.columns:
            df['creation_timestamp'] = df['creation_timestamp'].astype(str).apply(convert_timestamp)
            try:
                df.to_csv(file_path, index=False)
                print(f"Updated and saved: {file_name}")
            except Exception as e:
                print(f"Error saving file {file_name}: {e}")
        else:
            print(f"'creation_timestamp' column does not exist in {file_name}.")
