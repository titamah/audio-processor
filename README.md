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

## Utils

### File Manager
Provides functionality for exploring library directory and selecting files. The global variables specified are:

- **ROOT:** A constant variable for PathObject that is pointing to the ./library directory which stores all the audio files for the application
- **current_dir**: A PathObject for the current director a user is in
- **library**: A dict that stores PathObjects for each file and directory in the .library with its name as the key

The functions specified are:

- **print_library():** Prints the current directory and all its content
- **change_level(directory):** Moves the user from the current directory to the given PathObject
- **is_empty():** Returns a Bool if the library is empty or not
- **get_selection():** Prompts a user to navigate to the parent directory, exit the file manager, or input their selection from the library. 
- **select_item():** Prompts a user to make a selection. If the selection is a File, it will pass it to handler. If the selection is a Directory, it will recur. 
- **edit_file(file):** 
- **play_file(file):** 
- **delete_file(file):** Removes given file from Library and deletes file
- **rename_file(file, name):**
- **handle_selection(file):** Gets a selection and allows a prompts a user to edit, delete, listen, or deselect this file.

### Audio Tools
- **record():**
- **upload():**
- **play():**
- **save_as(Name):**
- **reverse(file)**
- **trim(file)**
- **change_volume(file, value)**
- **filter(file, filter, intensity?)**

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
