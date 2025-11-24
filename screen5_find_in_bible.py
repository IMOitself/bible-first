from bible_data import KJV_BIBLE
import time
import UI
from readchar import readkey, key
import shutil

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
                
                if query_lower in verse_text.lower():
                    results.append({
                        'book': book_name,
                        'chapter': chapter_num,
                        'verse': verse_num,
                        'text': verse_text
                    })
    return results

class BinarySearch:
    def recursive_search_verses(self, verses, book_name, chapter_num, query):
        if not verses:
            return []
            
        if len(verses) == 1:
            verse = verses[0]
            if query in verse['text'].lower():
                return [{
                    'book': book_name,
                    'chapter': chapter_num,
                    'verse': int(verse['verse']),
                    'text': verse['text']
                }]
            return []
            
        mid = len(verses) // 2
        left = self.recursive_search_verses(verses[:mid], book_name, chapter_num, query)
        right = self.recursive_search_verses(verses[mid:], book_name, chapter_num, query)
        return left + right

    def recursive_search_chapters(self, chapters, book_name, query):
        if not chapters:
            return []
        
        if len(chapters) == 1:
            return self.recursive_search_verses(chapters[0]['verses'], book_name, int(chapters[0]['chapter']), query)
            
        mid = len(chapters) // 2
        left = self.recursive_search_chapters(chapters[:mid], book_name, query)
        right = self.recursive_search_chapters(chapters[mid:], book_name, query)
        return left + right

    def search(self, query):
        results = []
        query_lower = query.lower()
        
        for book_data in KJV_BIBLE:
            # Loop through each book, then divide and conquer chapters
            book_results = self.recursive_search_chapters(book_data['chapters'], book_data['book'], query_lower)
            results.extend(book_results)
            
        return results

class IndexedSearch:
    def __init__(self):
        self.index = {}
        self.is_built = False
    
    def build_index(self):
        if self.is_built: return
        t0 = time.time()
        for book_data in KJV_BIBLE:
            book_name = book_data['book']
            for chapter_data in book_data['chapters']:
                c_num = int(chapter_data['chapter'])
                for verse_data in chapter_data['verses']:
                    v_num = int(verse_data['verse'])
                    text = verse_data['text']
                    
                    # Tokenize and index words
                    words = set(text.lower().split())
                    for w in words:
                        w_clean = w.strip('.,;:!?"()[]{}')
                        if not w_clean: continue
                        
                        if w_clean not in self.index:
                            self.index[w_clean] = []
                        
                        self.index[w_clean].append({
                            'book': book_name,
                            'chapter': c_num,
                            'verse': v_num,
                            'text': text
                        })
        self.is_built = True

    def search(self, query):
        if not self.is_built:
            self.build_index()
        
        query = query.lower().strip()
        results = []
        
        # Find all words in index that contain query (substring search support)
        matching_words = [w for w in self.index.keys() if query in w]
        
        seen_verses = set()
        for w in matching_words:
            for verse in self.index[w]:
                v_key = (verse['book'], verse['chapter'], verse['verse'])
                if v_key not in seen_verses:
                    seen_verses.add(v_key)
                    results.append(verse)
                    
        return results

def start():
    print("\033[H\033[2J")  # Clear screen
    word = input("enter word to search: ")
    print(f"\nSearching for '{word}'...")
    
    # Linear Search
    start_time = time.time()
    results_linear = search(word)
    end_time = time.time()
    linear_time = end_time - start_time
    
    # Binary Search
    binary_searcher = BinarySearch()
    start_time = time.time()
    results_binary = binary_searcher.search(word)
    end_time = time.time()
    binary_time = end_time - start_time
    
    # Indexed Search
    indexed_searcher = IndexedSearch()
    # Build first to separate build time
    start_time = time.time()
    indexed_searcher.build_index()
    end_time = time.time()
    build_time = end_time - start_time
    
    start_time = time.time()
    results_indexed = indexed_searcher.search(word)
    end_time = time.time()
    indexed_time = end_time - start_time

    # Use results_indexed for display
    match_results = results_indexed
    
    selected_row = 0
    scroll_offset = 0
    
    while True:
        print("\033[H\033[2J")  # Clear screen
        
        # Header
        UI.print_box(f'Results for "{word}"')
        
        print(f"Linear Search: {linear_time:.6f} seconds.")
        print(f"Binary Search: {binary_time:.6f} seconds.")
        print(f"Indexed Search Build: {build_time:.6f} seconds.")
        print(f"Indexed Search: {indexed_time:.6f} seconds.")
        print("-" * 40)

        # Calculate available space
        # Header takes roughly:
        # Box: 3 lines
        # Timings: 4 lines
        # Separator: 1 line
        # Footer ([Q] Back): 2 lines (newline + text)
        # Total reserved: ~10 lines.
        
        cols, rows = shutil.get_terminal_size()
        reserved_lines = 11
        list_height = max(1, rows - reserved_lines)
        
        # Adjust scroll offset to keep selected_row in view
        safe_capacity = max(1, list_height - 2)
        
        if selected_row < scroll_offset:
            scroll_offset = selected_row
        elif selected_row >= scroll_offset + safe_capacity:
             scroll_offset = selected_row - safe_capacity + 1
             
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
                # Highlight prefix
                # Truncate content if needed to fit one line
                
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
            
        # Fill empty lines if list is short
        rows_printed = len(visible_matches)
        if has_top_dots: rows_printed += 1
        if has_bottom_dots: rows_printed += 1
        
        if rows_printed < list_height:
            print("\n" * (list_height - rows_printed), end="")

        print("\n[Q] Back to Menu")
        
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