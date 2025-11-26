import os
from readchar import readkey, key
import UI
import textwrap

from bible_data import KJV_BIBLE


def get_verse_box(book_index, chapter_index, verse_index):
    # validate book index
    if book_index < 0 or book_index >= len(KJV_BIBLE):
        return ""
        
    book_data = KJV_BIBLE[book_index]
    book_name = book_data["book"]
    chapters = book_data["chapters"]
    
    # validate chapter index
    if chapter_index < 0: chapter_index = 0
    if chapter_index >= len(chapters): chapter_index = len(chapters) - 1
    
    chapter_data = chapters[chapter_index]
    verses = chapter_data["verses"]
    
    # validate verse index
    if verse_index < 0: verse_index = 0
    if verse_index >= len(verses): verse_index = len(verses) - 1
    
    verse_data = verses[verse_index]
    verse_num = verse_data["verse"]
    verse_text = verse_data["text"]
    
    chapter_num = chapter_data["chapter"]
    
    # wrap text for display
    wrapped_text = textwrap.fill(verse_text, width=50)

    import screen4_bookmarks
    is_bookmarked = False
    # check if current verse is bookmarked
    bookmarks = screen4_bookmarks.load_bookmarks()
    if bookmarks is not None:
        for bookmark in bookmarks:
            if bookmark[0] == book_index and bookmark[1] == chapter_index and bookmark[2] == verse_index:
                is_bookmarked = True
                break
    
    # build display text
    display_text = ""
    if is_bookmarked:
        display_text += "● "
    display_text += f"{book_name} {chapter_num}:{verse_num}\n"
    # display_text += f"{book_index}:{chapter_index}:{verse_index}\n" # debug hehe
    display_text += "King James Version\n\n"
    display_text += wrapped_text
    
    return display_text

def start(book_index, chapter_index, verse_index):
    # validate book index
    if book_index < 0 or book_index >= len(KJV_BIBLE):
        return

    while True:
        print("\033[H\033[2J")  # Clear screen
        
        # display the verse
        UI.print_box(get_verse_box(book_index, chapter_index, verse_index))
        
        print("[LEFT/RIGHT] Navigate [B] Bookmark [Q] Back")
        
        k = readkey()

        # toggle bookmark
        if k.lower() == 'b':
            import screen4_bookmarks
            is_bookmarked = False
            bookmarks = screen4_bookmarks.load_bookmarks()
            if bookmarks is not None:
                for bookmark in bookmarks:
                    if bookmark[0] == book_index and bookmark[1] == chapter_index and bookmark[2] == verse_index:
                        is_bookmarked = True
                        break
            
            if is_bookmarked:
                bookmarks.remove([book_index, chapter_index, verse_index])
            else:
                bookmarks.append([book_index, chapter_index, verse_index])
                
            screen4_bookmarks.save_bookmarks(bookmarks)

        else:
            is_bookmarked = False
        
        if k.lower() == 'q':
            break
            
        # previous verse
        elif k == key.LEFT:
            book_data = KJV_BIBLE[book_index]
            chapters = book_data["chapters"]
            verses = chapters[chapter_index]["verses"]
            
            if verse_index > 0:
                verse_index -= 1
            else:
                # go to previous chapter
                if chapter_index > 0:
                    chapter_index -= 1
                    prev_verses = chapters[chapter_index]["verses"]
                    verse_index = len(prev_verses) - 1

        # next verse
        elif k == key.RIGHT:
            book_data = KJV_BIBLE[book_index]
            chapters = book_data["chapters"]
            verses = chapters[chapter_index]["verses"]
            
            if verse_index < len(verses) - 1:
                verse_index += 1
            else:
                # go to next chapter
                if chapter_index < len(chapters) - 1:
                    chapter_index += 1
                    verse_index = 0

