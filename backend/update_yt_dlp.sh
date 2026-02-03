#!/bin/bash

cd /home/dolphins22/Documents/Dev/nas_music_downloader/backend/

# Update yt-dlp to latest
poetry update yt-dlp

# Commit the change only if there are changes
if git diff --quiet poetry.lock pyproject.toml; then
    echo "No changes to commit."
else
    git add poetry.lock pyproject.toml
    git commit -m "updated yt-dlp to latest"
    git push
    echo "yt-dlp updated to latest and changes pushed to remote."
fi

