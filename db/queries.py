from db.database import get_connection

def insert_note(note):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO audio_notes (name, file_path, created_at, folder, duration)
        VALUES (?, ?, ?, ?, ?)
    """, (note.name, note.file_path, note.created_at, note.folder, note.duration))

    conn.commit()
    conn.close()