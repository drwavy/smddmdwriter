# smddmdwriter
**Social Media Data Download Metadata Writer** is a Python-based utility designed to empower doomsday preppers, future linux users, data enthusiasts, and possibly even Bella Hadid, reclaim their personal media collections & data by reapplying metadata, preserving important information from Mark Zuckerberg's Goon Dungeon. It helps you enrich media files from social media data downloads with relevant metadata. This tool applies metadata ~date, caption, location information, and other EXIF tags directly to media files (images and videos) based on the data contained in JSON files that part of a social media data download package.

## Features:
- **Automatic Metadata Insertion**: Adds key metadata to media files, including original creation date, caption, and GPS coordinates.
- **Handles Social Media JSON Data**: Processes the JSON metadata files downloaded from social media platforms and applies relevant EXIF metadata to corresponding local media files.
- **UTF-8 Encoding Support**: Handles special characters and emojis in captions and ensures they are properly written into the EXIF data.
- **Skips External Content**: Automatically skips URIs pointing to externally hosted media ~Instagram-hosted videos.
- **Error Handling and Logging**: Comprehensive logging of actions and warnings ~missing URIs or skipped media files.

## Prerequisites:
- **Python 3.x** (download from [python.org](https://www.python.org/downloads/) if not already installed)
- **ExifTool** (installed via `brew install exiftool` on macOS or other package managers for Linux/Windows)
- **PyExifTool** (installed via `pip install -r requirements.txt`)
- **JSON metadata files**: Social media JSON data download must be in the original download format for the tool to work.

## Installation
1. **Install Python 3.x** from [python.org](https://www.python.org/downloads/)
2. **Install ExifTool**:
   macOS
   ```bash
   brew install exiftool
   ```
   Linux
   ```bash
   you already know how to do it
   ```
   Windows: Download and install from [ExifTool](https://exiftool.org/).

3. **Clone the smddmdwriter repository**.
   ```bash
   git clone https://github.com/drwavy/smddmdwriter.git
   ```
   
5. **Install Python dependencies**:
   Install the required Python packages by running:
   ```bash
   pip install -r requirements.txt
   ```
6. **Run** I use JetBrains so I just click the the green play button, if you don't use jetbrains I think you cd into smddmdwritter and write 'python main.py' or smth idk.


## Usage:
1. **Prepare your social media download data**:
   - Make sure your downloaded media and corresponding metadata (typically JSON files) are organized correctly in the original folder structure:
     - `base_folder/your_instagram_activity/content/` – For JSON metadata files
     - `base_folder/media/` – For media files (images and videos)
   
2. **Run the Script**:
   - Open a terminal (or command prompt) and navigate to the folder containing `smddmdwriter`.
   - Run the following command to start the script:
     ```bash
     python smddmdwriter.py
     ```

3. **Provide the Path to the Base Folder**:
   - When prompted, provide the absolute path to the base folder containing your social media download data.
   - Example:
     ```bash
     Please enter the path to the base folder: /absolute/path/to/base_folder/
     ```

4. **Review the Output**:
   - The script will process the media files and apply metadata where appropriate. A log file (`console_output.txt`) will be generated to track the actions taken and any warnings or skipped files.

## Logging:
- All console output, including errors, skipped files, and successful updates, will be logged in a file called `console_output.txt` in the directory where the script is run.
- Warnings will be issued for media files that cannot be found or external URIs that are skipped.

## Metadata Handled:
- **Date**: The `creation_timestamp` from the JSON file is used to set the following EXIF tags:
  - `DateTimeOriginal`
  - `CreateDate`
  - `ModifyDate`
  - `MediaCreateDate`
  - `MediaModifyDate`
  - `FileModifyDate`

- **Caption/Title**: The `title` from the JSON is written to the `Caption-Abstract` EXIF tag. Special characters and emojis are supported with UTF-8 encoding.

- **GPS Coordinates**: If available, `latitude` and `longitude` are written to the `GPSLatitude` and `GPSLongitude` EXIF tags.

## Known Limitations:
- **External URIs**: The script skips URIs that point to externally hosted content (e.g., media hosted on Instagram servers). It only processes local files that are found in the `media` folder.
- **Video Files**: Video files (`.mp4`, `.mov`, etc.) are skipped as they do not support EXIF metadata.
- **Unsupported JSON Formats**: The tool processes standard JSON formats found in most social media download packages. If the JSON structure differs significantly, the tool might not process it correctly.

## Troubleshooting:
- **Metadata Not Being Written**: Check that ExifTool is installed correctly and that the media files exist in the specified path. Check the `console_output.txt` for any warnings or errors.
- **Incorrect Captions**: If special characters in captions aren't showing correctly, check that the media file supports EXIF data and that you are using UTF-8 encoding.
- **Files Not Found**: Make sure the folder structure is correct and that media files are stored in the `media` folder under the base directory.

## Roadmap:
- **Current Status**: smddmdwriter currently supports only Instagram content JSON data downloads, specifically:
  - Posts
  - Archived Posts
  - Stories

- **Future Features**:
  - **Video Files**: Support for video files (`.mp4`, `.mov`, etc.)
  - **Messages**: Support for Instagram messages / inbox
  - **Wider Platform Support**: a wider range of social media data downloads, including:
    - **Instagram HTML Downloads**
    - **Snapchat JSON Data**
    - **Other Social Media Download Packages**
  
- **Rewriting in Perl**: Since ExifTool is written in Perl, the ultimate plan is to rewrite this utility in Perl. This will maximize efficiency and allow smddmdwriter to better interact with ExifTool, engaging in a harmonious marriage of code.

## License:
This project is licensed under the MIT License.

---
For any issues or questions, please refer to the troubleshooting section or contact the project maintainer.
