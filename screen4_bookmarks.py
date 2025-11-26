import json
import os
from readchar import readkey, key
import UI
import screen3_read_bible_verse
from bible_data import KJV_BIBLE

BOOKMARKS_FILE = "bookmarks.json"

def load_bookmarks():
    try:
        with open(BOOKMARKS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_bookmarks(bookmarks):
    with open(BOOKMARKS_FILE, "w") as f:
        json.dump(bookmarks, f)

def start():
    bookmarks = load_bookmarks()
    selected_index = 0

    while True:
        print("\033[H\033[2J")  # Clear screen

        if not bookmarks:
            print("\nBOOKMARKS\n")
            print("No bookmarks yet. press ENTER to start reading.")
            print("\n[Q] Back to Menu")
            k = readkey()
            if k.lower() == 'q':
                break
            elif k == key.ENTER:
                import screen3_read_bible_books
                screen3_read_bible_books.start()
            continue
        if selected_index >= len(bookmarks):
            selected_index = len(bookmarks) - 1
        if selected_index < 0:
            selected_index = 0

        current_bm = bookmarks[selected_index]
        UI.print_box(screen3_read_bible_verse.get_verse_box(current_bm[0], current_bm[1], current_bm[2]))

        print("\nBOOKMARKS\n")
        
        for i, bm in enumerate(bookmarks):
            book_idx, chap_idx, verse_idx = bm
            
            try:
                book_name = KJV_BIBLE[book_idx]["book"]
                display_chap = chap_idx + 1
                display_verse = verse_idx + 1
                
                line = f"{book_name} {display_chap}:{display_verse}"
            except:
                line = "Invalid Bookmark"

            if i == selected_index:
                print(f"\033[93m{line}\033[0m")
            else:
                print(f"{line}")

        print("\n[UP/DOWN] Navigate  [ENTER] Read  [D] Delete  [Q] Back")

        k = readkey()

        if k == key.UP:
            if selected_index > 0:
                selected_index -= 1
        elif k == key.DOWN:
            if selected_index < len(bookmarks) - 1:
                selected_index += 1
        elif k == key.ENTER:
            screen3_read_bible_verse.start(current_bm[0], current_bm[1], current_bm[2])
        elif k.lower() == 'd':
            bookmarks.pop(selected_index)
            save_bookmarks(bookmarks)
            if selected_index >= len(bookmarks) and selected_index > 0:
                selected_index -= 1
        elif k.lower() == 'q':
            break