from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play

def load_audio(file_path):
    return AudioSegment.from_file(file_path)


def play_audio(file_path):
    audio = load_audio(file_path)
    play(audio)


def reverse_audio(file_path):
    audio = load_audio(file_path)
    return audio.reverse()


def change_volume(file_path, db_change):
    audio = load_audio(file_path)
    return audio + db_change


def trim_audio(file_path, start_ms, end_ms):
    audio = load_audio(file_path)
    return audio[start_ms:end_ms]


def get_duration(file_path):
    audio = load_audio(file_path)
    return len(audio) / 1000
