import os
import UI
from bible_data import KJV_BIBLE
from readchar import readkey, key
import screen3_read_bible_verse

def print_number_grid(item_count, current_selection_index):
    """Prints a grid of numbers for chapters or verses."""
    # calculate total rows needed
    rows = (item_count + 9) // 10
    for row_index in range(rows):
        line_parts = []
        for col_index in range(10):
            # calculate current item index
            current_index = row_index * 10 + col_index
            if current_index < item_count:
                # format number with leading zero
                item_str = f"{current_index + 1:02}"
                # highlight selected item
                if current_index == current_selection_index:
                    item_str = f"\033[93m{item_str}\033[0m"
                line_parts.append(item_str)
            else:
                # empty space for padding
                line_parts.append("  ")
        print("  ".join(line_parts))

def handle_navigation(key_pressed, current_index, item_count):
    """Handles arrow key navigation for the grid."""
    # move up
    if key_pressed == key.UP:
        if current_index >= 10:
            return current_index - 10
            
    # move down
    elif key_pressed == key.DOWN:
        if current_index + 10 < item_count:
            return current_index + 10
        # handle last row edge case
        elif current_index + 10 >= item_count and current_index // 10 < (item_count - 1) // 10:
            return min(item_count - 1, current_index + 10)

    # move left
    elif key_pressed == key.LEFT:
        if current_index > 0:
            return current_index - 1

    # move right
    elif key_pressed == key.RIGHT:
        if current_index < item_count - 1:
            return current_index + 1
    return current_index

def start(book_index):
    """Main function to select chapter and verse."""
    # validate book index
    if not (0 <= book_index < len(KJV_BIBLE)): return

    book_data = KJV_BIBLE[book_index]
    book_name = book_data["book"]
    chapters = book_data["chapters"]
    
    selected_chapter_index = 0
    selected_verse_index = 0
    
    # Modes: 0 = Selecting Chapter, 1 = Selecting Verse
    selection_mode = 0 

    while True:
        print("\033[H\033[2J")  # Clear screen
        
        # chapter selection mode
        if selection_mode == 0:
            UI.print_box(f"{book_name} _:_")
            print("Chapter:")
            print_number_grid(len(chapters), selected_chapter_index)
        
        # verse selection mode
        elif selection_mode == 1:
            UI.print_box(f"{book_name} {selected_chapter_index + 1}:_")
            print("Verse:")
            current_chapter_data = chapters[selected_chapter_index]
            print_number_grid(len(current_chapter_data["verses"]), selected_verse_index)
            
        print("[ENTER] Select  [Q] Back")
        key_pressed = readkey()
        
        # back navigation
        if key_pressed.lower() == 'q':
            if selection_mode == 1: 
                # go back to chapter selection
                selection_mode = 0
            
            elif selection_mode == 0: 
                # exit to book list
                break
        
        # selection logic
        elif key_pressed == key.ENTER:
            if selection_mode == 0:
                # select chapter and switch to verse selection
                selection_mode = 1
                selected_verse_index = 0

            elif selection_mode == 1:
                # open the verse reader
                screen3_read_bible_verse.start(book_index, selected_chapter_index, selected_verse_index)

        else: # arrow keys
            if selection_mode == 0:
                selected_chapter_index = handle_navigation(key_pressed, selected_chapter_index, len(chapters))
            
            elif selection_mode == 1:
                current_chapter_data = chapters[selected_chapter_index]
                selected_verse_index = handle_navigation(key_pressed, selected_verse_index, len(current_chapter_data["verses"]))

if __name__ == "__main__":
    start(0)
