from pathlib import Path

p = Path('./library')

library = {
    (f.name + "/" if f.is_dir() else f.name): f 
    for f in p.glob('*') 
    if f.name != ".gitignore"
}

def print_library():
    for item in library.keys():
        print(item)

def change_level(d):
    global library 
    library = {
    (f.name + "/" if f.is_dir() else f.name): f 
    for f in d.glob('*') 
    if f.name != ".gitignore"
}

def is_empty():
    return not bool(library)

def get_selection():
    while True:
        i =  input("Enter the name of the item to select: ")
        if i in library:
            return library[i]
        print("This item doesn't exist! Try again.")
        print_library()

def select_item():
    item = get_selection()
    if item.is_dir():
        change_level(item)
        print_library()
        return select_item()
    elif item.is_file():
        return(item)
