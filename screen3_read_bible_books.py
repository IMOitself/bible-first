import shutil
import os


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
    


    columns = [column1, column2, column3]
    
    display_columns = []
    visible_ranges = []
    
    for i, column in enumerate(columns):
        offset = scroll_offsets[i]
        
        if is_tall_screen:
            window_size = 27
        else:
            window_size = max(1, rows_available)
            
        has_top_dots = offset > 0
        
        capacity = window_size
        if has_top_dots:
            capacity -= 1
            
        remaining_items = len(column) - offset
        
        if remaining_items > capacity:
            has_bottom_dots = True
            capacity -= 1
        else:
            has_bottom_dots = False
            
        start_idx = offset
        end_idx = min(len(column), offset + capacity)
        
        display_col = []
        if has_top_dots:
            display_col.append("...")
            
        current_slice = column[start_idx : end_idx]
        display_col.extend(current_slice)
        
        if has_bottom_dots:
            display_col.append("...")
            
        display_columns.append(display_col)
        visible_ranges.append((start_idx, end_idx))

    col_widths = []
    for column in display_columns:
        if not column:
            w = 0
        else:
            w = max(len(book) for book in column)
        col_widths.append(w + 2)

    max_row = max(len(column) for column in display_columns)
    
    for row in range(max_row):
        line_parts = []
        for col_idx in range(3):
            col = display_columns[col_idx]
            width = col_widths[col_idx]
            
            if row < len(col):
                item = col[row]
                item_text = item.ljust(width)
                
                if item != "...":
                    start_idx, _ = visible_ranges[col_idx]
                    has_top_dots = (scroll_offsets[col_idx] > 0)
                    
                    display_index = row
                    
                    slice_index = display_index - (1 if has_top_dots else 0)
                    
                    actual_index = start_idx + slice_index
                    
                    if col_idx == selected_col and actual_index == selected_row:
                        item_text = f"\033[93m{item_text}\033[0m"
            else:
                item_text = "".ljust(width)
            
            line_parts.append(item_text)
        print("".join(line_parts))
    
    return columns, visible_ranges

def start():
    print("\033[H\033[2J")  # Clear screen
    
    selected_col = 0
    selected_row = 0
    scroll_offsets = [0, 0, 0]
    
    while True:
        print("\033[H\033[2J")  # Clear screen
        
        _, rows = shutil.get_terminal_size()
        
        print("Books:")
        
        available_height = rows - 2
        books = get_book_names()
        
        is_tall = rows >= 30
        
        columns_data, visible_ranges = print_columns(books, available_height, is_tall, selected_col, selected_row, scroll_offsets)
        
        print("[Q] Back to Menu")
        
        k = readkey()
        if k.lower() == 'q':
            break
        
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
            book_index = -1
            if selected_col == 0:
                book_index = selected_row
            elif selected_col == 1:
                book_index = 27 + selected_row
            elif selected_col == 2:
                book_index = 39 + selected_row
                
            if book_index >= 0 and book_index < len(books):
                screen3_read_bible_chapters_and_verses.start(book_index)
            
        start_vis, end_vis = visible_ranges[selected_col]
        
        if selected_row < start_vis:
            scroll_offsets[selected_col] = selected_row
            
        elif selected_row >= end_vis:
            target_window = 27 if is_tall else available_height
            safe_capacity = max(1, target_window - 2)
            
            new_offset = max(0, selected_row - safe_capacity + 1)
            scroll_offsets[selected_col] = new_offset

if __name__ == "__main__":
    start()
