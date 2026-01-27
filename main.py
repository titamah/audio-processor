def main():
    print("Welcome to Audio Memos. Here you can create and manage your audio notes.")
    if len(memo_list) == 0:
        print("You have no audio memos.")
    else:
        for memo in memo_list:
            print(memo['title'])

memo_list = [{'title': 'Note1', 'location': 'path/to/note1'}, {'title': 'Note2', 'location': 'path/to/note2'}]

if __name__ == "__main__":
    main()