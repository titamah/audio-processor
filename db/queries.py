from db.database import get_connection
from models.audio_note import AudioNote

def insert_note(note):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO audio_notes (id, name, file_path, created_at, folder, duration)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (note.id, note.name, note.file_path, note.created_at, note.folder, note.duration))

    conn.commit()
    conn.close()


def get_library():
    conn = get_connection()
    cur = conn.cursor()

    rows = cur.execute("SELECT * FROM audio_notes").fetchall()
    notes = [AudioNote(*row) for row in rows]

    conn.commit()
    conn.close()
    
    return notes

def get_note(note_id):
    conn = get_connection()
    cur = conn.cursor()

    row = cur.execute(
        "SELECT * FROM audio_notes WHERE id = ?",
        (note_id,)
    ).fetchone()

    conn.close()

    if row is None:
        return None

    return AudioNote(*row)

def delete_note(note_id):
    conn = get_connection()
    cur = conn.cursor()

    note = get_note(note_id)

    if note:
        import os
        if os.path.exists(note.file_path):
            os.remove(note.file_path)

        cur.execute(
            "DELETE FROM audio_notes WHERE id = ?",
            (note_id,)
        )
    else:
        print("No note found")    
    
    conn.commit()
    conn.close()


def update_name(note_id, new_name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE audio_notes 
        SET name = ? 
        WHERE id = ?
    """, (new_name, note_id))
    
    conn.commit()
    conn.close()


def update_duration(note_id, new_duration):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE audio_notes
        SET duration = ?
        WHERE id = ?
    """, (new_duration, note_id))

    conn.commit()
    conn.close()