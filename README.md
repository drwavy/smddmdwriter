# smddmdwriter

**Social Media Data Download Metadata Writer**  
A utility that processes social media data exports, applies metadata to media items, and writes it into their EXIF and XMP schemas. This tool enables full compatibility with macOS Finder and Apple Photos by embedding metadata directly into media files, reducing reliance on external metadata storage.

## Prerequisites
- **Python 3.12** (Recommended). Download from [python.org](https://www.python.org/downloads/).
- **ExifTool**: ExifTool is installed and accessible from the command line.
- **JSON Metadata Files**: social media data download export is in its original downloaded format.

## Installation
Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/drwavy/smddmdwriter.git
cd smddmdwriter
python3 -m venv venv            # Create a virtual environment
source venv/bin/activate        # Activate the virtual environment (use 'venv\Scripts\activate' on Windows)
pip install -r requirements.txt # Install dependencies
```

> **Dependencies**: PyExifTool and Pandas are required, as specified in `requirements.txt`.

## Usage
1. **Prepare Social Media Download Data**  
   Organize your social media export files as follows:
   - `base_folder/your_instagram_activity/content/` – Contains JSON metadata files
   - `base_folder/media/` – Contains media files (images and videos)

2. **Run the Script**  
   From a terminal (or command prompt), navigate to the directory containing `smddmdwriter` and start the tool:

   ```bash
   python main.py
   ```

3. **Provide the Path to the Base Folder**  
   When prompted, enter the absolute path to the base folder containing your social media download data:
   
   ```plaintext
   Please enter the path to the base folder: /absolute/path/to/base_folder/
   ```

4. **Review the Output**  
   The script will process the media files, embedding metadata where applicable. A log file, `console_output.txt`, will be generated, capturing all actions, warnings, and any files that were skipped.

## Logging
- **console_output.txt**: All actions, errors, skipped files, and metadata updates are recorded in this log file for reference.

## Metadata Handled
The following metadata fields are processed and written to media files where applicable:

- **Date Information**: `creation_timestamp` is mapped to EXIF tags such as:
  - `DateTimeOriginal`, `CreateDate`, `ModifyDate`, `MediaCreateDate`, `MediaModifyDate`, and `FileModifyDate`

- **Caption/Title**: JSON `title` is written to the `Caption-Abstract` EXIF tag, supporting special characters and emojis via UTF-8 encoding.

- **GPS Coordinates**: If `latitude` and `longitude` are available, they are written to `GPSLatitude` and `GPSLongitude` EXIF tags.

## Known Limitations
- **External URIs**: Only local files in the `media` folder are processed; URIs pointing to external content are skipped.
- **Video Files**: Currently, video files (`.mp4`, `.mov`, etc.) are not processed due to limited EXIF metadata support.
- **Unsupported JSON Formats**: The tool is designed to process standard social media JSON formats. Significant structural variations in JSON files may cause processing issues.

## Scripts Overview
The following scripts are included in this repository to support various types of content:

- **apply_content.py**: Main application script for applying metadata to media files.
- **json2csv_*.py**: Series of conversion scripts for different content types, converting JSON metadata into CSV format for streamlined processing:
  - `json2csv_posts.py`, `json2csv_stories.py`, `json2csv_archived_posts.py`, `json2csv_igtv_videos.py`, `json2csv_reels.py`, and `json2csv_profile_photos.py`

## Roadmap
- **Supported Content**: Currently processes Instagram content JSON data for:
  - Posts, Archived Posts, Stories

- **Future Enhancements**:
  - Support for video metadata (`.mp4`, `.mov`, etc.)
  - Processing Instagram messages (inbox data)
  - Compatibility with additional platforms, such as:
    - **Instagram HTML Downloads**
    - **Snapchat JSON Data**
    - Other social media export formats

- **Rewriting in Perl**: To improve performance and better integrate with ExifTool, a future version may be implemented in Perl, ExifTool's native language.

## Troubleshooting
- **Metadata Not Written**: Verify ExifTool is installed and media files exist in the specified path.
- **Incorrect Captions**: media files support EXIF data and are encoded in UTF-8.
- **Files Not Found**: Confirm folder structure accuracy and correct placement of media files in the `media` folder.

## License
This project is licensed under the MIT License.

---

For questions or issues, please refer to the troubleshooting section or contact the project maintainer.
