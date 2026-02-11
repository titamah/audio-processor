from pathlib import Path

p = Path('./library')
files = list(p.glob('**/*'))

files = [x.name for x in files if x.name != ".gitignore"]

def get_files():
    for file in files:
        print(file)

def has_files():
    if len(files) == 0: 
        return False 
    else: 
        return True