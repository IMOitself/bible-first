from bible_data import KJV_BIBLE
import time
import UI
from readchar import readkey, key
import shutil
import re
import screen3_read_bible_verse

def search(query):
    results = []
    query_lower = query.lower()
    
    for book_data in KJV_BIBLE:
        book_name = book_data['book']
        for chapter_data in book_data['chapters']:
            chapter_num = int(chapter_data['chapter'])
            for verse_data in chapter_data['verses']:
                verse_num = int(verse_data['verse'])
                verse_text = verse_data['text']

                pattern = r'\b' + re.escape(query_lower) + r'(?:s|es)?\b'
                regex = re.compile(pattern, re.IGNORECASE)
                
                if regex.search(verse_text):
                    results.append({
                        'book': book_name,
                        'chapter': chapter_num,
                        'verse': verse_num,
                        'text': verse_text
                    })
    return results


def start():
    print("\033[H\033[2J")  # Clear screen
    word = input("enter word to search: ")
    print(f"\nSearching for '{word}'...")
    
    start_time = time.time()
    match_results = search(word)
    end_time = time.time()
    linear_time = end_time - start_time
    
    selected_row = 0
    scroll_offset = 0
    
    while True:
        print("\033[H\033[2J")  # Clear screen
        
        # Header
        UI.print_box(f'{len(match_results)} Results for "{word}"')
        
        print(f"found in {linear_time:.6f} seconds.")
        print("-" * 40)

        # Calculate available space
        cols, rows = shutil.get_terminal_size()
        reserved_lines = 11
        list_height = max(1, rows - reserved_lines)
        
        safe_capacity = max(1, list_height - 2)
        
        if selected_row < scroll_offset:
            scroll_offset = selected_row
        elif selected_row >= scroll_offset + safe_capacity:
           croll_offset = selected_row - safe_capacity + 1
             
        # Determine visible range
        has_top_dots = scroll_offset > 0
        
        capacity = list_height
        if has_top_dots:
            capacity -= 1
            
        remaining_items = len(match_results) - scroll_offset
        
        if remaining_items > capacity:
            has_bottom_dots = True
            capacity -= 1
        else:
            has_bottom_dots = False
            
        start_idx = scroll_offset
        end_idx = min(len(match_results), scroll_offset + capacity)
        
        visible_matches = match_results[start_idx : end_idx]
        
        if has_top_dots:
            print("...")
            
        # Print matches
        for i, match in enumerate(visible_matches):
            actual_index = start_idx + i
            
            prefix = f"{match['book']} {match['chapter']}:{match['verse']}"
            content = f" - {match['text']}"
            
            if actual_index == selected_row:
                full_line = f"{prefix}{content}"
                if len(full_line) > cols:
                    available_for_content = cols - len(prefix) - 4 # ... and margin
                    if available_for_content > 0:
                        content = content[:available_for_content] + "..."
                    else:
                        content = "" 
                
                print(f"\033[93m{prefix}\033[0m{content}")
            else:
                full_line = f"{prefix}{content}"
                if len(full_line) > cols:
                    full_line = full_line[:cols-3] + "..."
                print(full_line)
                
        if has_bottom_dots:
            print("...")

        print("[UP/DOWN] Navigate [ENTER] Read [Q] Back to Menu")
        
        k = readkey()
        if k.lower() == 'q':
            break
        elif k == key.UP:
            selected_row = max(0, selected_row - 1)
        elif k == key.DOWN:
            selected_row = min(len(match_results) - 1, selected_row + 1)
        elif k == key.ENTER:
            if match_results:
                selected_match = match_results[selected_row]
                
                # Find indices
                book_index = -1
                for i, b in enumerate(KJV_BIBLE):
                    if b['book'] == selected_match['book']:
                        book_index = i
                        break
                
                if book_index != -1:
                    chapter_index = selected_match['chapter'] - 1
                    verse_index = selected_match['verse'] - 1
                    
                    screen3_read_bible_verse.start(book_index, chapter_index, verse_index)

if __name__ == '__main__':
    start()