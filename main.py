import math
from pathlib import Path
import tempfile
import uuid
from pydub.playback import play
import sounddevice as sd
import soundfile as sf

import utils.file_manager as utils
from db.database import init_db
from db.queries import insert_note, get_library, delete_note, get_note, update_name
from services.audio_tools import change_volume, get_duration, play_audio, reverse_audio, trim_audio
from models.audio_note import AudioNote
from datetime import datetime

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import EmptyInputValidator, PathValidator


def view_library():
    notes = get_library()
    if len(notes) == 0:
        create = inquirer.confirm(message="The library is empty! Do you want to create an AudioNote?").execute()
        if create:
            add_file()
    else:
        choices = map(lambda note: Choice(name=f"{note.name:.<30} {datetime.fromisoformat(note.created_at).strftime("%m-%d-%y %I:%M %p"):.>5}", value=note.id),notes)
        select_note = inquirer.fuzzy(message="Select an AudioNote from your library:", choices=choices).execute()
        selection = get_note(select_note)
        view_note(selection)

def view_note(selection):
    print(f"{selection.name:.<30}{math.floor(selection.duration/60):0>2}:{round(selection.duration%60):0>2}")
    active = True
    while active:
        action = inquirer.fuzzy(message="Actions", choices=["Play","Edit", "Rename", "Delete", "Back"]).execute()
        if action == "Play":
            play_audio(selection.file_path)
        elif action == "Edit":
            edit_audio(selection)
        elif action == "Rename":
            name = inquirer.text(
                message="Name this audio note:",
                default=selection.name 
            ).execute()
            update_name(selection.id, name)
        elif action == "Delete":
            confirm = inquirer.confirm(message=f"Are you sure you want to delete {selection.name}?").execute()
            if confirm: 
                delete_note(selection.id)
                active = False
        elif action == "Back":
            active = False



def edit_audio(selection):
    print(f"{selection.name:.<30}{math.floor(selection.duration/60):0>2}:{round(selection.duration%60):0>2}")
    active = True
    while active:
        action = inquirer.fuzzy(message="Actions", choices=["Reverse","Volume", "Trim", "Back"]).execute()
        if action == "Play":
            play_audio(selection.file_path)
        elif action == "Reverse":
            audio = reverse_audio(selection.file_path)
            play(audio)
        elif action == "Volume":
            val = inquirer.number(
                message="Enter volume increment/decrement:",
                min_allowed=-10,
                max_allowed=10,
                validate=EmptyInputValidator(),
            ).execute()
            audio = change_volume(selection.file_path, val)
            play(audio)
        elif action == "Trim":
            start = inquirer.number(
                message="Enter starting point:",
                min_allowed=-10,
                max_allowed=10,
                validate=EmptyInputValidator(),
            ).execute()
            end = inquirer.number(
                message="Enter ending point:",
                min_allowed=0,
                max_allowed=get_duration(selection.file_path),
                validate=EmptyInputValidator(),
            ).execute()
            audio = trim_audio(selection.file_path, start, end)
            play(audio)
        elif action == "Back":
            active = False

        active = not confirm_edits(selection, audio)

def confirm_edits(selection, audio):
    active = True
    while active:
        confirm = inquirer.fuzzy(message="Save this version?", choices=["Play", "Overwrite this file","Create a new file", "Cancel"]).execute()
        if confirm == "Play":
            play(audio)
        elif confirm == "Overwrite this file":
            audio.export(selection.file_path, format="wav")
            return True
        elif confirm == "Create a new file":
            name = inquirer.text(
                message="Name this audio note:",
                default=selection.name 
            ).execute()
            note = AudioNote.create_new_audio(name, audio)
            insert_note(note)
            return True
        else:
            return False

def add_file():
    action = inquirer.select(message="Select an action:", choices=[Choice(name="Upload a file", value="upload"), Choice(name="Record a AudioNote", value="record"), Choice(name="Return to menu", value="return")]).execute()
    if action == "return":
        view_library()
        return
    elif action == "upload":
        src_path = inquirer.filepath(
            message="Enter file to upload:",
            validate=PathValidator(is_file=True, message="Input is not a file"),
            only_files=True,
        ).execute()
        src_path = src_path.strip("'\" ") 
        suggested_name = Path(src_path).stem
    elif action == "record":
        fs = 44100
        max_seconds = 900
        
        input("Press ENTER to start recording...")

        import time
        start_time = time.time()

        recording = sd.rec(int(max_seconds * fs), samplerate=fs, channels=1)
        
        print("Recording... (Press ENTER to stop)")
        input() 
        sd.stop()

        actual_duration = time.time() - start_time
        actual_frames = int(min(actual_duration, max_seconds) * fs)
        trimmed_recording = recording[:actual_frames]
        
        temp_dir = Path(tempfile.gettempdir())
        temp_path = temp_dir / f"rec_{uuid.uuid4().hex}.wav"
        print(f"DEBUG: sf is {sf}")
        sf.write(temp_path, trimmed_recording, fs)
        
        src_path = temp_path
        suggested_name = f"Recording {datetime.now().strftime('%b %d, %H:%M')}"

    name = inquirer.text(
        message="Name this audio note:",
        default=suggested_name 
    ).execute()

    note = AudioNote.create_new(name, src_path)
    insert_note(note)

def delete():
    i = input("Type in the ID for the audio note you want to delete: ")
    delete_note(i)

def main():
    init_db()
    active = True
    print("Welcome to Audio Notes. Here you can create and manage your audio notes.")
    while active:
        action = inquirer.select(message="Select an action:", choices=["View my notes", "Create a note", "Quit AudioNotes"]).execute()
        if action == "View my notes":
            view_library()
        elif action == "Create a note":
            add_file()
        elif action == "Quit AudioNotes":
            print("Quitting application...")
            active = not inquirer.confirm(message="Are you sure you want to exit the application?").execute()


if __name__ == "__main__":
    main()