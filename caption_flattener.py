import csv
import os

input_file = "csv/content.csv"
temp_file = "csv/temp_content.csv"  # Temporary file for intermediate processing

with open(input_file, mode="r", encoding="utf-8") as infile, open(temp_file, mode="w", encoding="utf-8", newline="") as outfile:
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)

    writer.writeheader()

    for row in reader:
        if "title" in row:
            row["title"] = " ".join(row["title"].replace("\r", " ").replace("\n", " ").split())
        writer.writerow(row)

os.replace(temp_file, input_file)

print(f"Processed CSV saved to {input_file}")
