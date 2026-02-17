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
            i = input(f"Are you sure you want to exit the file explorer? Enter Y for yes or N for no: ")
            if i.capitalize() == "Y":
                return False
            if i.capitalize() == "N":
                continue
        if i.capitalize() == "B":
            change_dir(current_dir.parent)
            continue
        if i in library:
            return library[i]
        print("This item doesn't exist! Try again.")

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
            library.pop(file.name).unlink()
            print("File deleted.")
            return True
        if i.capitalize() == "N":
            print("Canceled. Returning to menu.")
            return False
        print("Hm, I didn't catch that. Try again.")

def handle_selection(file):
    if not file.is_file():
        print("Hmm, this isn't file!")
    else:
        while True:
            print(f"--- Currect selection: : {file.name} ---")
            i = input("[E]dit, [D]elete, [L]isten, or [B]ack: ")
            if i.capitalize() == "E":
                edit_file(file)
            elif i.capitalize() == "D":
                if delete_file(file):
                    return False
            elif i.capitalize() == "L":
                play_file(file)
            elif i.capitalize() == "B":
                    continue
            else:
                print("Hm, I didn't catch that. Try again.")