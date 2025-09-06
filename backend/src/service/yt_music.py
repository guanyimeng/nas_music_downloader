import yt_dlp
import logging
import random
import os
import fnmatch
import json
from datetime import datetime

logger = logging.getLogger("yt_dlp downloader")

class yt_downloader:
    def __init__(self):
        self.__seed = random.randint(0, 2**32 - 1)
        self.__logger = logging.getLogger(yt_downloader.__name__)
        self.__output_folder = f'data/output/{self.__seed}/'
        self.output_filename =""
        self.output_musicname = ""
        self.download_status = ""

    def download_youtube_as_mp3(self, url) -> str:
        if os.path.exists(self.__output_folder):
            self.__logger.warning(f"Output folder already exists: {self.__output_folder}")
            for filename in os.listdir(self.__output_folder):
                file_path = os.path.join(self.__output_folder, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        self.__logger.info(f"Removed file: {file_path}")
                except Exception as e:
                    self.__logger.warning(f"Failed to remove file {file_path}: {e}")
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{self.__output_folder}/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': False,
                'noplaylist': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                logger.info(f"Downloading from URL: {url}")

            for filename in os.listdir(self.__output_folder):
                if fnmatch.fnmatch(filename, '*.mp3'):
                    self.output_filename = os.path.join(self.__output_folder, filename)
                    self.output_musicname = filename
                    self.download_status = "; Downloaded successfully ✅"
                    logger.info(f"Downloaded file: {self.output_filename}")
                    return self.output_filename
         
        except: 
            logger.error("Downloading failed")
            self.download_status = "; Download failed ❌"

# Testing
if __name__ == "__main__":
    youtube_url = input("Enter YouTube video URL: ")
    downloader = yt_downloader()
    output_file = downloader.download_youtube_as_mp3(youtube_url)
    if output_file:
        print(f"Downloaded file saved at: {output_file}")
    else:
        print("Download failed")
    