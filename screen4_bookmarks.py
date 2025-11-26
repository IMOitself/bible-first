import json
import os
from readchar import readkey, key
import UI
import screen3_read_bible_verse
from bible_data import KJV_BIBLE

BOOKMARKS_FILE = "bookmarks.json"

def load_bookmarks():
    if not os.path.exists(BOOKMARKS_FILE):
        return []
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
            print("No bookmarks yet. Add one from the Read Bible screen (press 'b').")
            print("\n[Q] Back to Menu")
            k = readkey()
            if k.lower() == 'q':
                break
            continue

        # Ensure selected index is valid
        if selected_index >= len(bookmarks):
            selected_index = len(bookmarks) - 1
        if selected_index < 0:
            selected_index = 0

        # Display the selected verse at the top
        current_bm = bookmarks[selected_index]
        # bookmarks are stored as [book_index, chapter_index, verse_index]
        screen3_read_bible_verse.print_verse_box(current_bm[0], current_bm[1], current_bm[2])

        print("\nBOOKMARKS\n")
        
        # Display list of bookmarks
        for i, bm in enumerate(bookmarks):
            book_idx, chap_idx, verse_idx = bm
            
            # Get readable name
            try:
                book_name = KJV_BIBLE[book_idx]["book"]
                # Display as 1-based for user if that's the convention, but indices are 0-based internally usually?
                # Looking at the data: "Chapter 3 (2), Verse 15 (14)" -> stored as [53, 2, 14]
                # So stored indices are 0-based.
                # Display should be 1-based.
                # Chapter 2 (index) is Chapter 3 (display).
                # Verse 14 (index) is Verse 15 (display).
                
                # Wait, let's double check the user request example:
                # # 1 Timothy 3:15
                # # 53th book, Chapter 3 (2), Verse 15 (14)
                # [53, 2, 14]
                
                # So we need to add 1 for display.
                display_chap = chap_idx + 1
                display_verse = verse_idx + 1
                
                line = f"{book_name} {display_chap}:{display_verse}"
            except:
                line = "Invalid Bookmark"

            if i == selected_index:
                print(f"\033[93m{line}\033[0m") # Inverted colors for selection
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
            # Open reading screen
            screen3_read_bible_verse.start(current_bm[0], current_bm[1], current_bm[2])
        elif k.lower() == 'd':
            bookmarks.pop(selected_index)
            save_bookmarks(bookmarks)
            if selected_index >= len(bookmarks) and selected_index > 0:
                selected_index -= 1
        elif k.lower() == 'q':
            break