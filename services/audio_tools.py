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


def change_speed(file_path, speed):
    audio = load_audio(file_path)
    altered = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * speed)
    }).set_frame_rate(audio.frame_rate)
    return altered


def get_duration(file_path):
    audio = load_audio(file_path)
    return len(audio) / 1000