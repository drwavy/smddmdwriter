# SMDDMDWRITER

**Social Media Data Download Metadata Writer**\
*Metadata is not Meta’s data!*

## Overview

SMDDMDWRITER makes it easy to organize and rewrite metadata back into your social media data exports. 
After your export is analyzed, it's neatly formatted and organized in a csv for you to make any edits you want. 
Your post captions, sender usernames, geolocation data, tagged users, date uploaded, mismanaged files, 
all processed and cleaned into two csv files. Utilizing kDMItems and Quicktime tags, SMDDMDWRTIER prepares media for 
Apple Photos and displaying accurate metadata in macOS Finder.

### Features
- Processes Instagram data exports in JSON and HTML formats.
- Organizes & formats metadata into clean CSV files for editing.
- Supports geolocation, captions, usernames, and tagging.
- Prepares media for Apple Photos, macOS Finder, and UNIX filesystem indexing.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-AGPL%20v3-red.svg)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-lightgrey)

## Installation & Usage

1. **Installation:**
    ```bash
   git clone https://github.com/drwavy/smddmdwriter.git
    ```
    ```bash
   cd smddmdwriter
    ```
    ```bash
   pip install -r requirements.txt
    ```
    ```bash
   python main.py
    ```

2. **Select Data Download Type**
   - Instagram HTML
   - Instagram JSON

3. **Edit Data _(optional)_**
   - Processed data will be saved in the `/csv` directory.
   - Save edits before continuing.

## Acknowledgments

This project would not have been possible without the contributions of the open-source community. 
The following libraries and tools played an essential role in its development:

- **[bs4 (v0.0.2)](https://pypi.org/project/bs4/)**: A lightweight wrapper around BeautifulSoup for web scraping.
- **[beautifulsoup4 (v4.12.3)](https://www.crummy.com/software/BeautifulSoup/)**: A powerful library for parsing HTML and XML documents.
- **[soupsieve (v2.6)](https://pypi.org/project/soupsieve/)**: A CSS selector library used to enhance HTML parsing with BeautifulSoup.
- **[pip (v24.3.1)](https://pip.pypa.io/)**: The Python package installer, enabling seamless dependency management.
- **[ftfy (v6.3.1)](https://pypi.org/project/ftfy/)**: A library for fixing Unicode issues in text processing.
- **[wcwidth (v0.2.13)](https://pypi.org/project/wcwidth/)**: A library for measuring the width of Unicode characters, critical for text formatting.
- **[pytz (v2024.2)](https://pypi.org/project/pytz/)**: A library for accurate timezone conversions and handling.
- **[numpy (v2.2.1)](https://numpy.org/)**: The fundamental package for numerical computing in Python.
- **[pandas (v2.2.3)](https://pandas.pydata.org/)**: A robust library for data manipulation and analysis.
- **[python-dateutil (v2.9.0.post0)](https://dateutil.readthedocs.io/)**: A library for powerful date and time manipulation.
- **[six (v1.17.0)](https://pypi.org/project/six/)**: A utility library for writing Python code compatible with both Python 2 and 3.

These libraries have been invaluable in addressing the challenges and implementing functionality efficiently. 



## License ![License](https://img.shields.io/badge/license-AGPL%20v3-red.svg)

This project is licensed under the **GNU Affero General Public License v3.0
(AGPL-3.0)**.

You are free to use, modify, and distribute this software under the terms of
the AGPL v3.0. For more information, see the [LICENSE](./LICENSE) file or
visit the [GNU official website](https://www.gnu.org/licenses/agpl-3.0.html).