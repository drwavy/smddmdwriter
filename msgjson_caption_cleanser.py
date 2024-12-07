import csv
import codecs
from unidecode import unidecode


def decode_text(input_text):
    try:
        decoded = codecs.decode(input_text.encode('latin1'), 'utf-8')
        normalized = unidecode(decoded)
        return normalized
    except Exception as e:
        print(f"Error decoding text: {e}")
        return input_text


def process_csv_inplace(input_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            rows = []
            for row in reader:
                if len(row) >= 3:
                    row[2] = decode_text(row[2])
                rows.append(row)

        with open(input_file, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(rows)

        print(f"Processed and overwritten file: {input_file}")
    except Exception as e:
        print(f"Error processing CSV: {e}")


input_csv = 'csv/messages_media.csv'

process_csv_inplace(input_csv)
