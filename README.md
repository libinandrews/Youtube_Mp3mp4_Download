
# YouTube Downloader

This is a Python script that allows you to download videos and audio from YouTube. It provides a graphical user interface (GUI) built with the tkinter library. The script utilizes the pytube library for downloading YouTube videos and playlists.

## Requirements

- Python 3.x
- Required packages: pytube, pandas, pyperclip, moviepy, requests

## Usage

1. Install the required packages by running the following command:
   ```
   pip install pytube pandas pyperclip moviepy requests
   ```

2. Run the script using the following command:
   ```
   python youtube_downloader.py
   ```

3. The YouTube Downloader GUI window will open.

4. Save Folder:
   - Click the "Choose Destination Folder" button to select the folder where you want to save the downloaded videos or audio.
   - The chosen folder path will be displayed below the button.

5. YouTube Data:
   - Enter the YouTube link in the provided text box.
   - You can either paste the link or manually type it.
   - Click the "Get Video Info" button to fetch information about the videos in the playlist or the single video.
   - The fetched video titles will be displayed in the dropdown menu.

6. Download:
   - Select the desired file type (MP3 or MP4) using the radio buttons.
   - Click the "Download" button to start downloading the selected videos or audio files.
   - The progress bar will indicate the download progress.

7. Disclaimer:
   - This script is intended for personal use only.
   - Please respect the YouTube terms of service and the rights of content creators.

## How to

- Choose the destination folder for downloaded files.
- Fetch video information from a YouTube playlist or a single video URL.
- Download either MP3 audio or MP4 video files.
- View progress bar for download status.
- Save and load settings for the destination folder.
- Display  video information to be downloaded in an Excel file.
- Clear downloaded data.
- Open the downloaded data in Excel.

