import utils.file_manager as utils

curr_dir = ""

def main():
    print("Welcome to Audio Memos. Here you can create and manage your audio notes.")
    if not utils.is_empty():
        print("Here are your saved memos:")
        ans = utils.select_item()
        utils.handle_selection(ans)
        print("Good job!!!")
    else:
        print("You don't have any memos saved! Record or upload one to get started.")

if __name__ == "__main__":
    main()