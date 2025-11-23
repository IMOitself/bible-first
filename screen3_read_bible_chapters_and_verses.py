import os
import sys
from readchar import readkey, key
import UI

try:
    from bible_data import KJV_BIBLE
except ImportError:
    print("Dependencies missing. Please ensure bible_data.py exists.")
    sys.exit(1)

def start(book_index):
    if book_index < 0 or book_index >= len(KJV_BIBLE):
        return

    book_data = KJV_BIBLE[book_index]
    book_name = book_data["book"]
    chapters = book_data["chapters"]
    num_chapters = len(chapters)
    
    selected_chapter_idx = 0
    selected_verse_idx = 0
    
    # Mode: 0 = Chapter Selection, 1 = Verse Selection
    mode = 0
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Header
        if mode == 0:
            UI.print_box(f"{book_name} _:_")
            print("Chapter:")
            
            # Grid Rendering for Chapters
            rows = (num_chapters + 9) // 10
            
            for r in range(rows):
                line_parts = []
                for c in range(10):
                    idx = r * 10 + c
                    if idx < num_chapters:
                        chapter_num = idx + 1
                        chapter_str = f"{chapter_num:02}"
                        
                        if idx == selected_chapter_idx:
                            chapter_str = f"\033[91m{chapter_str}\033[0m"
                        
                        line_parts.append(chapter_str)
                    else:
                        line_parts.append("  ")
                
                print("  ".join(line_parts))
                
        elif mode == 1:
            # Verse Selection Mode
            current_chapter_num = selected_chapter_idx + 1
            UI.print_box(f"{book_name} {current_chapter_num}:_")
            print("Verse:")
            
            # Get verses for selected chapter
            # chapters is a list of dicts: {"chapter": "1", "verses": [...]}
            chapter_data = chapters[selected_chapter_idx]
            verses = chapter_data["verses"]
            num_verses = len(verses)
            
            # Grid Rendering for Verses
            rows = (num_verses + 9) // 10
            
            for r in range(rows):
                line_parts = []
                for c in range(10):
                    idx = r * 10 + c
                    if idx < num_verses:
                        verse_num = idx + 1
                        verse_str = f"{verse_num:02}"
                        
                        if idx == selected_verse_idx:
                            verse_str = f"\033[91m{verse_str}\033[0m"
                        
                        line_parts.append(verse_str)
                    else:
                        line_parts.append("  ")
                
                print("  ".join(line_parts))
            
        print("\n[Q] Back")
        
        k = readkey()
        if k.lower() == 'q':
            if mode == 1:
                mode = 0
            else:
                break
        
        # Navigation
        if k == key.UP:
            if mode == 0:
                if selected_chapter_idx >= 10:
                    selected_chapter_idx -= 10
            else:
                if selected_verse_idx >= 10:
                    selected_verse_idx -= 10
                    
        elif k == key.DOWN:
            if mode == 0:
                if selected_chapter_idx + 10 < num_chapters:
                    selected_chapter_idx += 10
                elif selected_chapter_idx + 10 >= num_chapters and selected_chapter_idx // 10 < (num_chapters - 1) // 10:
                     selected_chapter_idx = min(num_chapters - 1, selected_chapter_idx + 10)
            else:
                # Verse mode down
                # Need to check num_verses
                # Re-fetch num_verses
                chapter_data = chapters[selected_chapter_idx]
                verses = chapter_data["verses"]
                num_verses = len(verses)
                
                if selected_verse_idx + 10 < num_verses:
                    selected_verse_idx += 10
                elif selected_verse_idx + 10 >= num_verses and selected_verse_idx // 10 < (num_verses - 1) // 10:
                     selected_verse_idx = min(num_verses - 1, selected_verse_idx + 10)
                 
        elif k == key.LEFT:
            if mode == 0:
                if selected_chapter_idx > 0:
                    selected_chapter_idx -= 1
            else:
                if selected_verse_idx > 0:
                    selected_verse_idx -= 1
                    
        elif k == key.RIGHT:
            if mode == 0:
                if selected_chapter_idx < num_chapters - 1:
                    selected_chapter_idx += 1
            else:
                # Re-fetch num_verses
                chapter_data = chapters[selected_chapter_idx]
                verses = chapter_data["verses"]
                num_verses = len(verses)
                
                if selected_verse_idx < num_verses - 1:
                    selected_verse_idx += 1
                    
        elif k == key.ENTER:
            if mode == 0:
                mode = 1
                selected_verse_idx = 0
            else:
                # Verse selected
                pass

if __name__ == "__main__":
    # Test with Genesis (Index 0)
    start(0)
