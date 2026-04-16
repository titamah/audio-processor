CREATE TABLE IF NOT EXISTS audio_notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    created_at TEXT NOT NULL,
    folder TEXT DEFAULT 'root',
    duration REAL
);