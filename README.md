### Current Update
All JSON parsing has been reduced from 14 files to just 2! Mashallah. 
Functions are now more modular, code is cleaner, God is Good.
One minor issue is the AAC files are being uncooperative.
I'm considering just converting them to mp4 as a part of the process.

# smddmdwriter ![Version](https://img.shields.io/badge/version-4.2.0--beta-orange.svg)

**smddmdwriter (Social Media Data Download Metadata Writer)** is a Python
utility that processes social media JSON exports, converting them into CSVs
for posts, stories, reels, IGTV videos, profile photos, and archived posts,
and embedding the metadata into media files using ExifTool. This ensures
compatibility with macOS Finder, Apple Photos, and other media management
tools by writing metadata directly into EXIF and XMP schemas, preserving
valuable context such as timestamps, locations, and descriptions.

## Prerequisites, Dependencies
- **Python**: Version 3.12 or higher
- **ExifTool**: Installed separately
- **Pandas**: Version 2.2.3 or higher
- **PyExifTool**: Version 0.5.6 or higher

## Installation
1. Verify your Python version. _Must have Python 3.12 or higher_.
    ```bash
    python --version
    ```
2. Verify **ExifTool** is installed on your system:
   - If not already installed, goto [ExifTool official website](https://exiftool.org/)
     for installation instructions.
3. Clone the repository:
    ```bash
    git clone https://github.com/drwavy/smddmdwriter.git
    cd smddmdwriter
    ```
4. Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. If zipped, **Unzip** your Instagram Data Download.

Instagram HTML
1. cd ightml
2. ightml.py - parse posts, archived posts, stories
3. ightmlw.py - apply metadata
4. ightmlmsg.py - parse inbox
5. ightmlmsg2.py - apply timestamp metadata
6. ightmlmsg3.py - apply caption metadata

## Configuration
- Paths to JSON files and media directories can be configured via script
  arguments or hardcoded per script.

## Contributing
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Roadmap
- Mann Tracht, Un Gott Lacht

## Acknowledgments
This project makes use of:
- [ExifTool](https://exiftool.org/) for metadata handling.
- [Pandas](https://pandas.pydata.org/) for data manipulation.
- [PyExifTool](https://pypi.org/project/pyexiftool/) for Python-based
  ExifTool integration.

## License ![License](https://img.shields.io/badge/license-AGPL%20v3-red.svg)

This project is licensed under the **GNU Affero General Public License v3.0
(AGPL-3.0)**.

You are free to use, modify, and distribute this software under the terms of
the AGPL v3.0. For more information, see the [LICENSE](./LICENSE) file or
visit the [GNU official website](https://www.gnu.org/licenses/agpl-3.0.html).
