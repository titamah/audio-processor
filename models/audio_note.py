from pathlib import Path
import uuid
from datetime import datetime
from pydub import AudioSegment

class AudioNote:
    def __init__(self, id, name, file_path, created_at, folder="root", duration=None):
        self.id = id
        self.name = name
        self.file_path = file_path
        self.created_at = created_at
        self.folder = folder
        self.duration = duration

    @classmethod    
    def create_new(cls, name, og_path):
        new_id = uuid.uuid4().hex
        new_path = f"./library/{new_id}.wav"
        audio = AudioSegment.from_file(Path(og_path))
        duration = len(audio) / 1000.0 
        audio.export(new_path, format="wav")

        return cls(new_id, name, new_path, datetime.now().isoformat(), "root", duration)
    
    @classmethod    
    def create_new_audio(cls, name, audio):
        new_id = uuid.uuid4().hex
        new_path = f"./library/{new_id}.wav"
        duration = len(audio) / 1000.0 
        audio.export(new_path, format="wav")

        return cls(new_id, name, new_path, datetime.now().isoformat(), "root", duration)
