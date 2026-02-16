import utils.file_manager as utils

def view_library():
    if utils.is_empty():
        print("You don't have any memos saved! Record or upload one to get started.")
        add_file()
    else:
        print("Here are your saved memos:")
        item = utils.select_item()
        if item is False:
            print("Returning to main menu...")

def add_file():
    print("We're adding a file!")

def main():
    active = True
    print("Welcome to Audio Memos. Here you can create and manage your audio notes.")
    while active:
        i = input("[V]iew your memos, [A]dd a new one, or [Q]uit: ")
        if i.capitalize() == "V":
            view_library()
        elif i.capitalize() == "A":
            add_file()
        elif i.capitalize() == "Q":
            print("See you next time! Quitting application...")
            active = False
        else:
            print("Oops, I didn't catch that! Try again.")

    


if __name__ == "__main__":
    main()