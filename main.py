import utils.file_manager as utils

def view_library():
    return False

def record_file():
    return False

def main():
    print("Welcome to Audio Memos. Here you can create and manage your audio notes.")
    if not utils.is_empty():
        print("Here are your saved memos:")
        if not utils.select_item():
            print("Bye bye!")
    else:
        print("You don't have any memos saved! Record or upload one to get started.")

if __name__ == "__main__":
    main()