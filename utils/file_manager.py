from pathlib import Path

root = Path('./library')
curr_dir = root

library = {
    (f.name + "/" if f.is_dir() else f.name): f 
    for f in root.glob('*') 
    if f.name != ".gitignore"
}

def print_library():
    print(curr_dir.relative_to(root))
    for item in library.keys():
        print("- " + item)

def change_level(d):
    global library, curr_dir 
    curr_dir = d
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
        i =  input("Enter the name of the item to select: ")
        if i.capitalize() == "B":
            change_level(curr_dir.parent)
            return curr_dir
        if i in library:
            return library[i]
        print("This item doesn't exist! Try again.")

def select_item():
    item = get_selection()
    if item.is_dir():
        change_level(item)
        return select_item()
    elif item.is_file():
        return(item)
    
def edit_file(file):
    print("Pretend you're editing this file!")
    handle_selection(file)

    
def play_file(file):
    print("Pretend you're listening to this file.")
    handle_selection(file)

def delete_file(file):
    while True:
        i = input(f"Are you sure you want to delete {file.name}? Enter Y for yes or N for no: ")
        if i.capitalize() == "Y":
            library.pop(file.name).unlink()
            print("File deleted.")
            return True
        if i.capitalize() == "N":
            print("Canceled. Returning to menu.")
            handle_selection(file)
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
                    select_item()
            elif i.capitalize() == "L":
                play_file(file)
            elif i.capitalize() == "B":
                select_item()
            print("Hm, I didn't catch that. Try again.")