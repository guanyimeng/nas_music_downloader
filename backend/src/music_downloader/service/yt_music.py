import yt_dlp
import logging
import re
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path
from dataclasses import dataclass

from ..config.settings import settings

@dataclass
class DownloadResult:
    """Result of a download operation"""
    success: bool
    file_path: Optional[str] = None
    title: Optional[str] = None
    artist: Optional[str] = None
    duration: Optional[float] = None
    file_size: Optional[int] = None
    error_message: Optional[str] = None

class MusicDownloader:
    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir or settings.output_directory)
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for filesystem compatibility"""
        # Remove or replace invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Remove multiple spaces and trim
        filename = re.sub(r'\s+', ' ', filename).strip()
        # Limit length
        if len(filename) > 200:
            filename = filename[:200] + "..."
        return filename
    
    def _extract_metadata(self, info: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'title': info.get('title', '').strip(),
            'artist': info.get('uploader', '').strip() or info.get('creator', '').strip(),
            'duration': info.get('duration'),  # in seconds
            'description': info.get('description', ''),
            'upload_date': info.get('upload_date'),
            'view_count': info.get('view_count'),
            'webpage_url': info.get('webpage_url'),
        }
    
    def download_audio(self, url: str) -> DownloadResult:
        try:
            # Create unique subdirectory for this download
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            download_dir = self.output_dir / f"download_{timestamp}"
            download_dir.mkdir(exist_ok=True)
            
            # Configure yt-dlp options
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(download_dir / '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
                'no_warnings': False,
                'noplaylist': True,
                'extractaudio': True,
                'audioformat': 'mp3',
                'embed_subs': False,
                'writesubtitles': False,
                'writeautomaticsub': False,
            }
            
            # Download and extract info
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract info first
                info = ydl.extract_info(url, download=False)
                if not info:
                    return DownloadResult(
                        success=False,
                        error_message="Could not extract video information"
                    )
                
                # Extract metadata
                metadata = self._extract_metadata(info)
                self.logger.info(f"Downloading: {metadata['title']} by {metadata['artist']}")
                
                # Perform download
                ydl.download([url])
                
                # Find the downloaded MP3 file
                mp3_files = list(download_dir.glob("*.mp3"))
                if not mp3_files:
                    return DownloadResult(
                        success=False,
                        error_message="No MP3 file found after download"
                    )
                
                # Get the first (and should be only) MP3 file
                output_file = mp3_files[0]
                
                # Sanitize filename and move to final location
                sanitized_name = self._sanitize_filename(f"{metadata['title']}.mp3")
                final_path = self.output_dir / sanitized_name
                
                # Handle filename conflicts
                counter = 1
                while final_path.exists():
                    name_part = sanitized_name.rsplit('.', 1)[0]
                    final_path = self.output_dir / f"{name_part}_{counter}.mp3"
                    counter += 1
                
                # Move file to final location
                output_file.rename(final_path)
                
                # Clean up temporary directory
                try:
                    download_dir.rmdir()
                except OSError:
                    # Directory not empty, clean up remaining files
                    for file in download_dir.iterdir():
                        file.unlink()
                    download_dir.rmdir()
                
                # Get file size
                file_size = final_path.stat().st_size if final_path.exists() else None
                
                self.logger.info(f"Successfully downloaded: {final_path}")
                
                return DownloadResult(
                    success=True,
                    file_path=str(final_path),
                    title=metadata['title'],
                    artist=metadata['artist'],
                    duration=metadata['duration'],
                    file_size=file_size
                )
                
        except yt_dlp.DownloadError as e:
            error_msg = f"Download failed: {str(e)}"
            self.logger.error(error_msg)
            return DownloadResult(success=False, error_message=error_msg)
            
        except Exception as e:
            error_msg = f"Unexpected error during download: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return DownloadResult(success=False, error_message=error_msg)

# For testing
if __name__ == "__main__":
    # url = input("Enter video URL: ")
    url = "https://www.youtube.com/watch?v=IhuPnNYQyLk"
    downloader = MusicDownloader()
    result = downloader.download_audio(url)
    
    if result.success:
        print(f"Downloaded: {result.title}")
        print(f"File: {result.file_path}")
        print(f"Artist: {result.artist}")
        print(f"Duration: {result.duration}s")
        print(f"Size: {result.file_size} bytes")
    else:
        print(f"Download failed: {result.error_message}")
    