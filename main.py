import math
from pathlib import Path
import tempfile
import uuid
from pydub.playback import play
import sounddevice as sd
import soundfile as sf

from db.database import init_db
from db.queries import insert_note, get_library, delete_note, get_note, update_name, update_duration
from services.audio_tools import change_volume, get_duration, play_audio, reverse_audio, change_speed
from models.audio_note import AudioNote
from datetime import datetime

from InquirerPy import inquirer, get_style
from InquirerPy.base.control import Choice
from InquirerPy.validator import EmptyInputValidator, PathValidator
from InquirerPy.utils import color_print


# ── Palette ───────────────────────────────────────────────────────────────────
STYLE = get_style({
    "questionmark":       "#9b8dff bold",   # purple prompt marker
    "answermark":         "#9b8dff",
    "question":           "#e8e8e8 bold",   # bright white question text
    "answered_question":  "#6b6b6b",        # dim after answering
    "answer":             "#9b8dff",        # purple selected answer echo
    "pointer":            "#9b8dff bold",   # purple arrow
    "input":              "#e8e8e8",
    "instruction":        "#5c5c5c",        # dim gray hints
    "validator":          "#e06c75",
    "fuzzy_prompt":       "#9b8dff",
    "fuzzy_match":        "#9b8dff bold",
    "fuzzy_info":         "#5c5c5c",
    "marker":             "#9b8dff",
}, style_override=False)

# ── Typography helpers ─────────────────────────────────────────────────────────
PURPLE = "#9b8dff"
DIM    = "#5c5c5c"
WHITE  = "#e8e8e8"
ACCENT = "#c3b8ff"

def print_header():
    color_print([
        (f"bold {PURPLE}", "♪ Audio Notes"),
        ("", "  "),
        (DIM, "your personal voice library\n"),
    ])

def print_note_line(note):
    mins = math.floor(note.duration / 60)
    secs = round(note.duration % 60)
    color_print([
        (f"bold {WHITE}",  f"  {note.name}"),
        (DIM,              "  ·  "),
        (ACCENT,           f"{mins:0>2}:{secs:0>2}\n"),
    ])


# ── Library ────────────────────────────────────────────────────────────────────
def view_library():
    notes = get_library()
    if len(notes) == 0:
        create = inquirer.confirm(
            message="Your library is empty. Create an AudioNote?",
            style=STYLE
        ).execute()
        if create:
            add_file()
    else:
        choices = list(map(
            lambda note: Choice(
                name=f"{note.name:.<32}{datetime.fromisoformat(note.created_at).strftime('%m-%d-%y %I:%M %p'):>14}",
                value=note.id
            ),
            notes
        ))
        select_note = inquirer.fuzzy(
            message="Your Library  (type to search)",
            choices=choices,
            style=STYLE,
        ).execute()
        selection = get_note(select_note)
        view_note(selection)


# ── Note view ──────────────────────────────────────────────────────────────────
def view_note(selection):
    print_note_line(selection)
    active = True
    while active:
        action = inquirer.select(
            message=f"{selection.name}",
            choices=["Play", "Edit", "Rename", "Delete", "Back"],
            style=STYLE,
        ).execute()
        if action == "Play":
            play_audio(selection.file_path)
        elif action == "Edit":
            edit_audio(selection)
        elif action == "Rename":
            name = inquirer.text(
                message="New name:",
                default=selection.name,
                style=STYLE,
            ).execute()
            update_name(selection.id, name)
            selection.name = name
        elif action == "Delete":
            confirm = inquirer.confirm(
                message=f"Delete \"{selection.name}\"? This can't be undone.",
                style=STYLE,
            ).execute()
            if confirm:
                delete_note(selection.id)
                active = False
        elif action == "Back":
            active = False


# ── Edit ───────────────────────────────────────────────────────────────────────
def edit_audio(selection):
    print_note_line(selection)
    active = True
    while active:
        action = inquirer.select(
            message=f"Editing  ·  {selection.name}",
            choices=["Reverse", "Volume", "Speed", "Back"],
            style=STYLE,
        ).execute()
        audio = None
        if action == "Reverse":
            audio = reverse_audio(selection.file_path)
        elif action == "Volume":
            val = inquirer.number(
                message="Volume change (dB):",
                min_allowed=-10,
                max_allowed=10,
                validate=EmptyInputValidator(),
                style=STYLE,
            ).execute()
            audio = change_volume(selection.file_path, val)
        elif action == "Speed":
            speed = inquirer.select(
                message="Playback speed:",
                choices=[
                    Choice(name="0.5x  — half speed",   value=0.5),
                    Choice(name="0.75x — slow",          value=0.75),
                    Choice(name="1.25x — slightly fast", value=1.25),
                    Choice(name="1.5x  — fast",          value=1.5),
                    Choice(name="2x    — double speed",  value=2.0),
                ],
                style=STYLE,
            ).execute()
            audio = change_speed(selection.file_path, speed)
        elif action == "Back":
            active = False

        if audio is not None:
            saved = confirm_edits(selection, audio)
            if saved:
                active = False


def confirm_edits(selection, audio):
    while True:
        confirm = inquirer.select(
            message="Save this version?",
            choices=["Play", "Overwrite original", "Save as new note", "Cancel"],
            style=STYLE,
        ).execute()
        if confirm == "Play":
            play(audio)
        elif confirm == "Overwrite original":
            audio.export(selection.file_path, format="wav")
            update_duration(selection.id, len(audio) / 1000.0)
            return True
        elif confirm == "Save as new note":
            name = inquirer.text(
                message="Name this note:",
                default=selection.name,
                style=STYLE,
            ).execute()
            note = AudioNote.create_new_audio(name, audio)
            insert_note(note)
            return True
        else:
            return False


# ── Add file ───────────────────────────────────────────────────────────────────
def add_file():
    action = inquirer.select(
        message="Add an AudioNote",
        choices=[
            Choice(name="Upload a file",    value="upload"),
            Choice(name="Record a new note", value="record"),
            Choice(name="Back to menu",      value="return"),
        ],
        style=STYLE,
    ).execute()

    if action == "return":
        return
    elif action == "upload":
        src_path = inquirer.filepath(
            message="File path:",
            validate=PathValidator(is_file=True, message="Input is not a file"),
            only_files=True,
            style=STYLE,
        ).execute()
        src_path = src_path.strip("'\" ")
        suggested_name = Path(src_path).stem
    elif action == "record":
        fs = 44100
        max_seconds = 900

        input("  Press ENTER to start recording...")

        import time
        start_time = time.time()
        recording = sd.rec(int(max_seconds * fs), samplerate=fs, channels=1)

        color_print([(f"bold {PURPLE}", "  ● Recording  "), (DIM, "press ENTER to stop\n")])
        input()
        sd.stop()

        actual_duration = time.time() - start_time
        actual_frames = int(min(actual_duration, max_seconds) * fs)
        trimmed_recording = recording[:actual_frames]

        temp_dir = Path(tempfile.gettempdir())
        temp_path = temp_dir / f"rec_{uuid.uuid4().hex}.wav"
        sf.write(temp_path, trimmed_recording, fs)

        src_path = temp_path
        suggested_name = f"Recording {datetime.now().strftime('%b %d, %H:%M')}"

    name = inquirer.text(
        message="Name this note:",
        default=suggested_name,
        style=STYLE,
    ).execute()

    note = AudioNote.create_new(name, src_path)
    insert_note(note)
    color_print([(f"bold {PURPLE}", f"  ✓ Saved  "), (DIM, f"{name}\n")])


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    init_db()
    print_header()
    active = True
    while active:
        action = inquirer.select(
            message="What would you like to do?",
            choices=["View my notes", "Create a note", "Quit"],
            style=STYLE,
        ).execute()
        if action == "View my notes":
            view_library()
        elif action == "Create a note":
            add_file()
        elif action == "Quit":
            confirm = inquirer.confirm(message="Exit Audio Notes?", style=STYLE).execute()
            if confirm:
                color_print([(DIM, "  bye ♪\n")])
                active = False


if __name__ == "__main__":
    main()