import os
import UI
from bible_data import KJV_BIBLE
from readchar import readkey, key
import screen3_read_bible_verse

def print_grid(num_items, selected_idx):
    rows = (num_items + 9) // 10
    for r in range(rows):
        line_parts = []
        for c in range(10):
            idx = r * 10 + c
            if idx < num_items:
                item_str = f"{idx + 1:02}"
                if idx == selected_idx:
                    item_str = f"\033[93m{item_str}\033[0m"
                line_parts.append(item_str)
            else:
                line_parts.append("  ")
        print("  ".join(line_parts))

def handle_navigation(k, current_idx, total_items):
    if k == key.UP:
        if current_idx >= 10:
            return current_idx - 10
    elif k == key.DOWN:
        if current_idx + 10 < total_items:
            return current_idx + 10
        elif current_idx + 10 >= total_items and current_idx // 10 < (total_items - 1) // 10:
            return min(total_items - 1, current_idx + 10)
    elif k == key.LEFT:
        if current_idx > 0:
            return current_idx - 1
    elif k == key.RIGHT:
        if current_idx < total_items - 1:
            return current_idx + 1
    return current_idx

def start(book_index):
    if not (0 <= book_index < len(KJV_BIBLE)): return

    book_data = KJV_BIBLE[book_index]
    book_name = book_data["book"]
    chapters = book_data["chapters"]
    
    selected_chapter = 0
    selected_verse = 0
    mode = 0 # 0: Chapter, 1: Verse

    while True:
        print("\033[H\033[2J")  # Clear screen
        
        if mode == 0:
            UI.print_box(f"{book_name} _:_")
            print("Chapter:")
            print_grid(len(chapters), selected_chapter)
        else:
            UI.print_box(f"{book_name} {selected_chapter + 1}:_")
            print("Verse:")
            print_grid(len(chapters[selected_chapter]["verses"]), selected_verse)
            
        print("\n[Q] Back")
        k = readkey()
        
        if k.lower() == 'q':
            if mode == 1: mode = 0
            else: break
        elif k == key.ENTER:
            if mode == 0:
                mode = 1
                selected_verse = 0
            else:
                screen3_read_bible_verse.start(book_index, selected_chapter, selected_verse)
        else:
            if mode == 0:
                selected_chapter = handle_navigation(k, selected_chapter, len(chapters))
            else:
                selected_verse = handle_navigation(k, selected_verse, len(chapters[selected_chapter]["verses"]))

if __name__ == "__main__":
    start(0)
