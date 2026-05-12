# Audio Notes
A command-line application to record, upload, and manage audio notes.

# Features
- Record new audio notes directly from the microphone
- Upload existing audio files into your library
- Browse and search your library
- Play back any saved note
- Rename or delete notes
- Edit notes: reverse, adjust volume, change playback speed
- Save edits as a new note or overwrite the original

# Tech Stack
- **PyDub** — audio manipulation (reverse, volume, speed, export)
- **FFmpeg** — audio encoding/decoding (required by PyDub)
- **sounddevice** — microphone recording
- **soundfile** — writing recorded audio to disk
- **SQLite** — local database for storing note metadata
- **InquirerPy** — interactive CLI prompts and styling

# Project Structure
```
.
├── main.py                  # App entry point and all UI logic
├── audio_notes.db           # SQLite database (auto-created on first run)
├── library/                 # Stored audio files (.wav)
├── db/
│   ├── database.py          # Connection and DB initialization
│   ├── queries.py           # All SQL queries (insert, get, update, delete)
│   └── schema.sql           # Table definitions
├── models/
│   └── audio_note.py        # AudioNote class
└── services/
    └── audio_tools.py       # Audio manipulation functions
```

# Database
SQLite via the built-in `sqlite3` module. The database is initialized on startup via `init_db()`, which runs `schema.sql` if the table doesn't exist yet.

### Schema
```sql
CREATE TABLE IF NOT EXISTS audio_notes (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    file_path TEXT,
    created_at TEXT NOT NULL,
    folder TEXT DEFAULT 'root',
    duration REAL
);
```

### Queries (`db/queries.py`)
- **insert_note(note)** — saves a new AudioNote to the DB
- **get_library()** — returns all notes as AudioNote objects
- **get_note(note_id)** — returns a single note by ID
- **delete_note(note_id)** — removes note from DB and deletes its file from disk
- **update_name(note_id, new_name)** — renames a note
- **update_duration(note_id, new_duration)** — updates duration after edits that change length (e.g. speed change)

# AudioNote Model (`models/audio_note.py`)
Represents a single audio note.

### Fields
- `id` — unique hex ID (uuid4)
- `name` — user-given name
- `file_path` — path to the `.wav` file in `./library/`
- `created_at` — ISO timestamp
- `folder` — reserved for future folder organization (default `'root'`)
- `duration` — length in seconds (float)

### Class Methods
- **create_new(name, og_path)** — loads audio from a source path (upload or temp recording), exports it to `./library/`, computes duration, returns a new AudioNote instance
- **create_new_audio(name, audio)** — same but takes a PyDub AudioSegment directly (used when saving edited audio)

# Audio Tools (`services/audio_tools.py`)
- **load_audio(file_path)** — loads a file as a PyDub AudioSegment
- **play_audio(file_path)** — loads and plays a file
- **reverse_audio(file_path)** — returns reversed AudioSegment
- **change_volume(file_path, db_change)** — returns AudioSegment with adjusted volume (±dB)
- **change_speed(file_path, speed)** — returns AudioSegment at new speed (0.5x–2x) using frame rate manipulation
- **get_duration(file_path)** — returns duration in seconds

# Requirements
- Python 3.7+
- FFmpeg installed on your system
- See `requirements.txt` for Python packages