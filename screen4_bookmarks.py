import json
import os
from readchar import readkey, key
import UI
import screen3_read_bible_verse
from bible_data import KJV_BIBLE

import random
from recommended_verses import verses as recommended_verses_data

# file to store bookmarks
BOOKMARKS_FILE = "bookmarks.json"

# load bookmarks from file
def load_bookmarks():
    try:
        with open(BOOKMARKS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

# save bookmarks to file
def save_bookmarks(bookmarks):
    with open(BOOKMARKS_FILE, "w") as f:
        json.dump(bookmarks, f)

def start():
    bookmarks = load_bookmarks()
    
    # Randomly select 5 recommended verses
    recommended_selection = random.sample(recommended_verses_data, min(5, len(recommended_verses_data)))
    
    selected_index = 0

    while True:
        print("\033[H\033[2J")  # Clear screen

        total_items = len(bookmarks) + len(recommended_selection)
        
        # ensure selected index is valid
        if selected_index >= total_items:
            selected_index = total_items - 1
        if selected_index < 0:
            selected_index = 0

        # Determine which verse to display in the box
        if selected_index < len(bookmarks):
            current_bm = bookmarks[selected_index]
        else:
            current_bm = recommended_selection[selected_index - len(bookmarks)]
            
        UI.print_box(screen3_read_bible_verse.get_verse_box(current_bm[0], current_bm[1], current_bm[2]))

        print("\nBOOKMARKS:")
        
        if not bookmarks:
            print("No bookmarks yet.")
        else:
            # list all bookmarks
            for i, bm in enumerate(bookmarks):
                book_idx, chap_idx, verse_idx = bm
                
                try:
                    book_name = KJV_BIBLE[book_idx]["book"]
                    display_chap = chap_idx + 1
                    display_verse = verse_idx + 1
                    
                    line = f"{book_name} {display_chap}:{display_verse}"
                except:
                    line = "Invalid Bookmark"

                # highlight selected bookmark
                if i == selected_index:
                    print(f"\033[93m\033[7m{line}\033[0m")
                else:
                    print(f"{line}")

        print("\nRECOMMENDED VERSES:")
        
        # list recommended verses
        for i, bm in enumerate(recommended_selection):
            global_index = len(bookmarks) + i
            book_idx, chap_idx, verse_idx = bm
            
            try:
                book_name = KJV_BIBLE[book_idx]["book"]
                display_chap = chap_idx + 1
                display_verse = verse_idx + 1
                
                line = f"{book_name} {display_chap}:{display_verse}"
            except:
                line = "Invalid Verse"

            # highlight selected recommended verse
            if global_index == selected_index:
                print(f"\033[93m\033[7m{line}\033[0m")
            else:
                print(f"{line}")

        print("\n[UP/DOWN] Navigate  [ENTER] Read  [D] Delete  [Q] Back")

        k = readkey()

        # navigation
        if k == key.UP:
            if selected_index > 0:
                selected_index -= 1
        elif k == key.DOWN:
            if selected_index < total_items - 1:
                selected_index += 1
        
        # open selected verse
        elif k == key.ENTER:
            screen3_read_bible_verse.start(current_bm[0], current_bm[1], current_bm[2])
            
        # delete bookmark (only if a bookmark is selected)
        elif k.lower() == 'd':
            if selected_index < len(bookmarks):
                bookmarks.pop(selected_index)
                save_bookmarks(bookmarks)
                # Adjust selection if needed
                if selected_index >= len(bookmarks) + len(recommended_selection):
                     selected_index -= 1
                
        # back to menu
        elif k.lower() == 'q':
            break