# Audio Memos
A command-line application that allows users to record and upload audio files.

# Features
- record new audio files and save them
- upload audio files to the application
- view saved audio files and play them back
- manipulate / edit an audio file (ex: increase or decrease volume, reverse, trim)

# Requirements
- PyDub for audio manipulation
- FFmpeg for AudioFile coding and decoding
- sounddevice for recording and playback

# Implementation
- Files will be stored in ./library/ directory
- Users can upload or record files directly into this directory
- ./utlis/file_manager.py provides functions for getting, viewing, and listing out files stored in Memo