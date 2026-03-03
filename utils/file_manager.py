from pathlib import Path

ROOT = Path('./library')
current_dir = ROOT

library = {
    (f.name + "/" if f.is_dir() else f.name): f 
    for f in ROOT.glob('*') 
    if f.name != ".gitignore"
}

def print_library():
    print(current_dir.relative_to(ROOT))
    for item in library.keys():
        print("- " + item)

def change_dir(d):
    global library, current_dir 
    if not d.is_relative_to(ROOT):
        print("You are already at the root.")
    else:
        current_dir = d
        library = {
        (f.name + "/" if f.is_dir() else f.name): f 
        for f in d.glob('*') 
        if f.name != ".gitignore"
}

def is_empty():
    return not bool(library)

def get_selection():
    while True:
        print_library()
        i =  input("Enter [B]ack, [E]xit, or the name of the item: ")
        if i.capitalize() == "E":
            confirm = input(f"Are you sure you want to exit the file explorer? Enter Y for yes or N for no: ")
            if confirm.capitalize() == "Y":
                return False
            if i.capitalize() == "N":
                continue
        elif i.capitalize() == "B":
            change_dir(current_dir.parent)
            continue
        else:
            try:
                return library[i]
            except KeyError:
                print(f"Error: '{i}' doesn't exist.")

def select_item():
    item = get_selection()
    if item is False:
        return False
    elif item.is_dir():
        change_dir(item)
        return select_item()
    elif item.is_file():
        print("Selected: " + item.name)
        if handle_selection(item) is False:
            return select_item()
    
def edit_file(file):
    print("Pretend you're editing this file!")
    
def play_file(file):
    print("Pretend you're listening to this file.")

def delete_file(file):
    while True:
        i = input(f"Are you sure you want to delete {file.name}? Enter Y for yes or N for no: ")
        if i.capitalize() == "Y":
            try:
                library.pop(file.name).unlink()
                print("File deleted.")
                return True
            except KeyError:
                print(f"Error: '{i}' file not found.")
                return False
            except OSError as error:
                print(f"Error: {error.strerror}")
                return False
        if i.capitalize() == "N":
            print("Canceled. Returning to menu.")
            return False
        print("Hm, I didn't catch that. Try again.")

def handle_selection(file):
    try:
        if not file.is_file():
            raise ValueError("Selection is not a file.")
        else:
            while True:
                print(f"--- Currect selection: : {file.name} ---")
                i = input("[E]dit, [D]elete, [L]isten, or [B]ack: ")
                try:
                    if i.capitalize() == "E":
                        edit_file(file)
                    elif i.capitalize() == "D":
                        if delete_file(file):
                            return False
                    elif i.capitalize() == "L":
                        play_file(file)
                    elif i.capitalize() == "B":
                            return False
                    else:
                        print("Hm, I didn't catch that. Try again.")
                except Exception as e:
                    print(f"Error: {e}")
    except ValueError as error:
        print(f"Error: {error}")
    except FileNotFoundError:
        print("Error: File not found.")