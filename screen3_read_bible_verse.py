import os
from readchar import readkey, key
import UI
import textwrap

from bible_data import KJV_BIBLE


def get_verse_box(book_index, chapter_index, verse_index):
    if book_index < 0 or book_index >= len(KJV_BIBLE):
        return ""
        
    book_data = KJV_BIBLE[book_index]
    book_name = book_data["book"]
    chapters = book_data["chapters"]
    
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
    
    wrapped_text = textwrap.fill(verse_text, width=50)
    
    display_text = f"{book_name} {chapter_num}:{verse_num}" + f" {book_index}:{chapter_index}:{verse_index}\n"
    display_text += "King James Version\n\n"
    display_text += wrapped_text
    
    return display_text

def start(book_index, chapter_index, verse_index):
    if book_index < 0 or book_index >= len(KJV_BIBLE):
        return

    while True:
        print("\033[H\033[2J")  # Clear screen
        
        UI.print_box(get_verse_box(book_index, chapter_index, verse_index))
        
        print("[<-] Before [->] After [Q] Back")
        
        k = readkey()
        
        if k.lower() == 'q':
            break
            
        elif k == key.LEFT:
            book_data = KJV_BIBLE[book_index]
            chapters = book_data["chapters"]
            verses = chapters[chapter_index]["verses"]
            
            if verse_index > 0:
                verse_index -= 1
            else:
                if chapter_index > 0:
                    chapter_index -= 1
                    prev_verses = chapters[chapter_index]["verses"]
                    verse_index = len(prev_verses) - 1

        elif k == key.RIGHT:
            book_data = KJV_BIBLE[book_index]
            chapters = book_data["chapters"]
            verses = chapters[chapter_index]["verses"]
            
            if verse_index < len(verses) - 1:
                verse_index += 1
            else:
                if chapter_index < len(chapters) - 1:
                    chapter_index += 1
                    verse_index = 0

