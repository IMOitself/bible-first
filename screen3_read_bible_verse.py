import os
import sys
from readchar import readkey, key
import UI
import textwrap

from bible_data import KJV_BIBLE
from readchar import readkey, key

def start(book_index, chapter_index, verse_index):
    if book_index < 0 or book_index >= len(KJV_BIBLE):
        return

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        book_data = KJV_BIBLE[book_index]
        book_name = book_data["book"]
        chapters = book_data["chapters"]
        
        # Safety check for indices
        if chapter_index < 0: chapter_index = 0
        if chapter_index >= len(chapters): chapter_index = len(chapters) - 1
        
        chapter_data = chapters[chapter_index]
        verses = chapter_data["verses"]
        
        if verse_index < 0: verse_index = 0
        if verse_index >= len(verses): verse_index = len(verses) - 1
        
        verse_data = verses[verse_index]
        verse_num = verse_data["verse"]
        verse_text = verse_data["text"]
        
        chapter_num = chapter_data["chapter"]
        
        # Format the text for the box
        # We'll wrap the text to fit nicely within a reasonable width, e.g., 50 chars
        wrapped_text = textwrap.fill(verse_text, width=50)
        
        display_text = f"{book_name} {chapter_num}:{verse_num}\n"
        display_text += "King James Version\n\n"
        display_text += wrapped_text
        
        UI.print_box(display_text)
        
        print("[<-] Before [->] After [Q] Back")
        
        k = readkey()
        
        if k.lower() == 'q':
            break
            
        elif k == key.LEFT:
            # Go to previous verse
            if verse_index > 0:
                verse_index -= 1
            else:
                # Go to previous chapter?
                if chapter_index > 0:
                    chapter_index -= 1
                    # Go to last verse of previous chapter
                    verse_index = len(chapters[chapter_index]["verses"]) - 1
                else:
                    # Previous book? For now just stop at start of book
                    pass
                    
        elif k == key.RIGHT:
            # Go to next verse
            if verse_index < len(verses) - 1:
                verse_index += 1
            else:
                # Go to next chapter?
                if chapter_index < len(chapters) - 1:
                    chapter_index += 1
                    verse_index = 0
                else:
                    # Next book? For now just stop at end of book
                    pass
