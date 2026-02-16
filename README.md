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

Next Steps:
In Main: Allow user to go in and out of Read/Update/Delete mode to Create Mode
Create Mode:
Create a Utils/audio_manipulation or something
- record, upload from a computer
- select file > add to library
- Do you want to listen?
- save as > do you want to overwrite?

In Edit mode:
- play, delete, edit
- edit > rename, reverse, trim, change volume, filter
- change volume > + X or - X
- filer > list out filter options
- Do you want to listen?
- Do you want to edit or you're done?
- Save a copy or overwrite?
- save a copy > input name
- add to library

Add all functions so far to README
- name
- input, output
- description
