CREATE TABLE IF NOT EXISTS audio_notes (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    file_path TEXT,
    created_at TEXT NOT NULL,
    folder TEXT DEFAULT 'root',
    duration REAL
);