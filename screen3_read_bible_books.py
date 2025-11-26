import shutil
import os
from bible_data import KJV_BIBLE
from readchar import readkey, key
import screen3_read_bible_chapters_and_verses

def get_book_names():
    """Returns a list of all book names from the Bible data."""
    return [book["book"] for book in KJV_BIBLE]

def print_3_columns(books, available_rows, is_tall_screen, selected_column_index, selected_row_index, scroll_offsets):
    """
    Prints the Bible books in 3 columns.
    Handles scrolling and highlighting the selected book.
    """
    old_testament_books = books[:39] # the 39th and everything before it
    new_testament_books = books[39:] # everything after the 39th

    # we limit it to 27 to display all new testament books in the last column
    # the check is done before calling this, so we assume we have space.
    rows_per_column = 27

    # 2 columns for Old Testament
    # 1 column for New Testament
    column_1_data = old_testament_books[:rows_per_column]
    column_2_data = old_testament_books[rows_per_column:]
    column_3_data = new_testament_books
    
    all_columns = [column_1_data, column_2_data, column_3_data]
    
    # prepare data for display (handling scrolling)
    display_columns = []
    visible_ranges = [] # To track which indices are currently visible
    
    for i in range(3):
        current_column_data = all_columns[i]
        current_scroll_offset = scroll_offsets[i]
        
        # determine how many items we can show in this column
        if is_tall_screen:
            window_height = 27 # show full height if screen is tall enough
        else:
            window_height = max(1, available_rows)
            
        # check if we need "..." indicators
        has_content_above = current_scroll_offset > 0
        
        # calculate capacity (space for items)
        capacity = window_height
        if has_content_above:
            capacity -= 1 # reserve space for top "..."
            
        remaining_items = len(current_column_data) - current_scroll_offset
        
        if remaining_items > capacity:
            has_content_below = True
            capacity -= 1 # reserve space for bottom "..."
        else:
            has_content_below = False
            
        # calculate the slice of data to show
        start_index = current_scroll_offset
        end_index = min(len(current_column_data), current_scroll_offset + capacity)
        
        # build the list of items to display for this column
        items_to_display = []
        if has_content_above:
            items_to_display.append("...")
            
        items_slice = current_column_data[start_index : end_index]
        items_to_display.extend(items_slice)
        
        if has_content_below:
            items_to_display.append("...")
            
        display_columns.append(items_to_display)
        visible_ranges.append((start_index, end_index))

    # calculate column widths for alignment
    column_widths = []
    for column_items in display_columns:
        if not column_items:
            width = 0
        else:
            # find the longest string in this column
            width = max(len(item) for item in column_items)
        column_widths.append(width + 2) # add some padding

    # print the rows
    max_display_rows = max(len(col) for col in display_columns)
    
    for row_index in range(max_display_rows):
        line_parts = []
        for col_index in range(3):
            column_items = display_columns[col_index]
            width = column_widths[col_index]
            
            if row_index < len(column_items):
                item_text = column_items[row_index]
                padded_text = item_text.ljust(width)
                
                # check if this item is the selected one
                if item_text != "...":
                    # we need to map the display row back to the actual data index to check selection
                    start_vis, _ = visible_ranges[col_index]
                    has_top_dots = (scroll_offsets[col_index] > 0)
                    
                    # adjust index based on whether "..." is present
                    offset_adjustment = 1 if has_top_dots else 0
                    actual_data_index = start_vis + row_index - offset_adjustment
                    
                    if col_index == selected_column_index and actual_data_index == selected_row_index:
                        # highlight selected item in yellow
                        padded_text = f"\033[93m\033[7m{padded_text}\033[0m"
            else:
                # empty space if this column has fewer rows
                padded_text = "".ljust(width)
            
            line_parts.append(padded_text)
        print("".join(line_parts))
    
    return all_columns, visible_ranges

def start():
    """Main function to run the Bible Books screen."""
    print("\033[H\033[2J")  # Clear screen
    
    selected_column_index = 0
    selected_row_index = 0
    scroll_offsets = [0, 0, 0] # track scroll position for each column
    
    while True:
        print("\033[H\033[2J")  # clear screen
        
        # get terminal size
        columns, rows = shutil.get_terminal_size()
        
        print("Books:")
        
        # calculate available height for the list
        available_height = rows - 2 # subtract space for header and footer
        
        all_books = get_book_names()
        
        # check if screen is tall enough to show everything without scrolling
        is_tall_screen = rows >= 30
        
        # print the columns and get back data needed for navigation
        columns_data, visible_ranges = print_3_columns(
            all_books, 
            available_height, 
            is_tall_screen, 
            selected_column_index, 
            selected_row_index, 
            scroll_offsets
        )
        
        print("\n[ENTER] Select [Q] Back to Menu")
        
        # handle user input
        key_pressed = readkey()
        
        if key_pressed.lower() == 'q':
            break
        
        # navigation logic
        if key_pressed == key.UP:
            selected_row_index = max(0, selected_row_index - 1)
            
        elif key_pressed == key.DOWN:
            # prevent going past the last item in the current column
            current_column_length = len(columns_data[selected_column_index])
            selected_row_index = min(current_column_length - 1, selected_row_index + 1)
            
        elif key_pressed == key.LEFT:
            selected_column_index = max(0, selected_column_index - 1)
            # adjust row if the new column is shorter
            current_column_length = len(columns_data[selected_column_index])
            selected_row_index = min(current_column_length - 1, selected_row_index)
            
        elif key_pressed == key.RIGHT:
            selected_column_index = min(2, selected_column_index + 1)
            # adjust row if the new column is shorter
            current_column_length = len(columns_data[selected_column_index])
            selected_row_index = min(current_column_length - 1, selected_row_index)
            
        elif key_pressed == key.ENTER:
            # calculate the global index of the selected book
            book_global_index = -1
            if selected_column_index == 0:
                book_global_index = selected_row_index
            elif selected_column_index == 1:
                book_global_index = 27 + selected_row_index # 27 is the length of column 1
            elif selected_column_index == 2:
                book_global_index = 39 + selected_row_index # 39 is length of col 1 + col 2
                
            if 0 <= book_global_index < len(all_books):
                screen3_read_bible_chapters_and_verses.start(book_global_index)
            
        # scrolling logic
        # ensure the selected item is visible
        start_visible, end_visible = visible_ranges[selected_column_index]
        
        if selected_row_index < start_visible:
            # scroll up
            scroll_offsets[selected_column_index] = selected_row_index
            
        elif selected_row_index >= end_visible:
            # scroll down
            # we want the selected item to be at the bottom of the view
            target_window_height = 27 if is_tall_screen else available_height
            # reserve space for "..." if needed (approximate)
            safe_capacity = max(1, target_window_height - 2) 
            
            new_offset = max(0, selected_row_index - safe_capacity + 1)
            scroll_offsets[selected_column_index] = new_offset

if __name__ == "__main__":
    start()
