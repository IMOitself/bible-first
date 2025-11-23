import shutil
import os
import sys

from bible_data import KJV_BIBLE
from readchar import readkey, key
import screen3_read_bible_chapters_and_verses

def get_book_names():
    return [b["book"] for b in KJV_BIBLE]

def print_columns(books, rows_available, is_tall_screen, selected_col, selected_row, scroll_offsets):
    ot_books = books[:39] # Genesis to Malachi
    nt_books = books[39:] # Matthew to Revelation
    
    # we limit it to 27 to display all new testament books in the last column
    # the check is done before calling this, so we assume we have space.
    row_limit = 27

    # column distribution
    # 2 columns for Old Testament
    # 1 column for New Testament
    column1 = ot_books[:row_limit]
    column2 = ot_books[row_limit:]
    column3 = nt_books
    
    if not is_tall_screen:
        # On small screens, we don't limit the logical column size, 
        # we just limit the display window.
        # So the columns remain full length.
        pass

    columns = [column1, column2, column3]
    
    display_columns = []
    visible_ranges = [] # Store (start_index, end_index) for each column
    
    for i, column in enumerate(columns):
        offset = scroll_offsets[i]
        
        # Determine available slots for this column
        # If is_tall_screen, we just show everything (or up to 27)
        # But the logic for 'is_tall_screen' was to force 27 limit.
        # If not tall, we use rows_available.
        
        if is_tall_screen:
            # In tall mode, we assume it fits? 
            # The original code had `row_limit = 27` fixed.
            # But if we have scrolling, we should just use rows_available as the window?
            # Let's stick to the original logic: if tall, we show full columns (up to 27).
            # If not tall, we scroll.
            window_size = 27
        else:
            window_size = max(1, rows_available)
            
        # Calculate what fits
        # We need to determine if we need top dots and bottom dots
        
        has_top_dots = offset > 0
        
        # Initial guess at capacity
        capacity = window_size
        if has_top_dots:
            capacity -= 1
            
        # Check if we need bottom dots
        # If remaining items > capacity
        remaining_items = len(column) - offset
        
        if remaining_items > capacity:
            has_bottom_dots = True
            capacity -= 1 # Reserve space for bottom dots
        else:
            has_bottom_dots = False
            
        # Slice
        start_idx = offset
        end_idx = min(len(column), offset + capacity)
        
        # Build display list
        display_col = []
        if has_top_dots:
            display_col.append("...")
            
        # Add actual items
        # We need to track the actual index for highlighting
        current_slice = column[start_idx : end_idx]
        display_col.extend(current_slice)
        
        if has_bottom_dots:
            display_col.append("...")
            
        display_columns.append(display_col)
        visible_ranges.append((start_idx, end_idx))

    # calculate widths
    col_widths = []
    for column in display_columns:
        if not column:
            w = 0
        else:
            w = max(len(book) for book in column)
        col_widths.append(w + 2) # +2 for padding

    # print rows
    max_row = max(len(column) for column in display_columns)
    
    for row in range(max_row):
        line_parts = []
        for col_idx in range(3):
            col = display_columns[col_idx]
            width = col_widths[col_idx]
            
            if row < len(col):
                item = col[row]
                item_text = item.ljust(width)
                
                # Check highlighting
                if item != "...":
                    # We need to find the actual index of this item
                    # We can infer it from the visible_ranges
                    start_idx, _ = visible_ranges[col_idx]
                    has_top_dots = (scroll_offsets[col_idx] > 0)
                    
                    # The index in the display list
                    display_index = row
                    
                    # The index in the slice (skipping top dots)
                    slice_index = display_index - (1 if has_top_dots else 0)
                    
                    actual_index = start_idx + slice_index
                    
                    if col_idx == selected_col and actual_index == selected_row:
                        item_text = f"\033[91m{item_text}\033[0m"
            else:
                item_text = "".ljust(width)
            
            line_parts.append(item_text)
        print("".join(line_parts))
    
    return columns, visible_ranges

def start():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    selected_col = 0
    selected_row = 0
    scroll_offsets = [0, 0, 0]
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        cols, rows = shutil.get_terminal_size()
        
        print("Books:")
        
        available_height = rows - 2
        books = get_book_names()
        
        is_tall = rows >= 30
        
        columns_data, visible_ranges = print_columns(books, available_height, is_tall, selected_col, selected_row, scroll_offsets)
        
        print("[Q] Back to Menu")
        
        k = readkey()
        if k.lower() == 'q':
            break
        
        # Navigation Logic
        if k == key.UP:
            selected_row = max(0, selected_row - 1)
        elif k == key.DOWN:
            selected_row = min(len(columns_data[selected_col]) - 1, selected_row + 1)
        elif k == key.LEFT:
            selected_col = max(0, selected_col - 1)
            selected_row = min(len(columns_data[selected_col]) - 1, selected_row)
        elif k == key.RIGHT:
            selected_col = min(2, selected_col + 1)
            selected_row = min(len(columns_data[selected_col]) - 1, selected_row)
            
        elif k == key.ENTER:
            # Calculate book index
            # Col 0: 0-26 (27 items) -> index = row
            # Col 1: 27-38 (12 items) -> index = 27 + row
            # Col 2: 39+ (NT) -> index = 39 + row
            
            # We need to account for scrolling!
            # The `selected_row` is the logical index in the column (0 to len(column)-1).
            # So we don't need to worry about scroll_offsets here, as selected_row tracks the logical position.
            
            book_index = -1
            if selected_col == 0:
                book_index = selected_row
            elif selected_col == 1:
                book_index = 27 + selected_row
            elif selected_col == 2:
                book_index = 39 + selected_row
                
            if book_index >= 0 and book_index < len(books):
                screen3_read_bible_chapters_and_verses.start(book_index)
            
        # Update Scroll Offsets
        # Check if selected_row is within visible range
        start_vis, end_vis = visible_ranges[selected_col]
        
        # Note: end_vis is exclusive
        # If selected_row is < start_vis, we need to scroll up
        if selected_row < start_vis:
            scroll_offsets[selected_col] = selected_row
            
        # If selected_row is >= end_vis, we need to scroll down
        elif selected_row >= end_vis:
            # We need to bring selected_row into view.
            # The easiest way is to set the offset such that selected_row is the last visible item.
            # But calculating the exact offset is tricky because of dynamic "..."
            # A simple heuristic: increment offset until it fits? 
            # Or just set offset = selected_row - (window_size - padding)
            
            # Let's try a conservative jump
            # If we just increment offset, it might take multiple frames if the user held the key, 
            # but here we process one key at a time.
            # Let's try setting offset to `selected_row - (available_height - 3)`
            # available_height is roughly the window size.
            
            target_window = 27 if is_tall else available_height
            # Reserve space for dots (approx 2)
            safe_capacity = max(1, target_window - 2)
            
            new_offset = max(0, selected_row - safe_capacity + 1)
            scroll_offsets[selected_col] = new_offset

if __name__ == "__main__":
    start()
