from datetime import datetime

class AudioNote:
    def __init__(self, id, name, file_path, created_at, folder="root", duration=None):
        self.id = id
        self.name = name
        self.file_path = file_path
        self.created_at = created_at
        self.folder = folder
        self.duration = duration