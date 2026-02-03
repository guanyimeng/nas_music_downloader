#!/bin/bash

cd /home/dolphins22/Documents/Dev/nas_music_downloader/backend/

# Update yt-dlp to latest
poetry update yt-dlp

# Commit the change
git add poetry.lock poetry.toml
git commit -m "updated yt-dlp to latest"

# Push to remote
git push

echo "yt-dlp updated to latest and changes pushed to remote."