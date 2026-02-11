import utils.file_manager as utils

def main():
    print("Welcome to Audio Memos. Here you can create and manage your audio notes.")
    if utils.has_files():
        print("Here are your saved memos:")
        utils.get_files()
    else:
        print("You don't have any memos saved! Record or upload one to get started.")

if __name__ == "__main__":
    main()