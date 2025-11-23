from typing import List, Tuple, Optional
import shutil
import textwrap
from readchar import readkey, key
import UI

try:
    from bible_data import KJV_BIBLE
except Exception:
    print("\033[H\033[2J", end="")
    print("KJV Bible data not found.")
    input("Press Enter...")
    exit()

def clear_screen():
    print("\033[H\033[2J", end="")

def get_book_chapter(book_idx: int, chap_idx: int):
    try:
        book = KJV_BIBLE[book_idx]
        chapter = book["chapters"][chap_idx]
        book_name = book.get("book", "UNKNOWN")
        chapter_number = chapter.get("chapter", str(chap_idx + 1))
        verses = chapter.get("verses", [])
        return book_name, chapter_number, verses
    except Exception:
        return "UNKNOWN", str(chap_idx + 1), []

def get_verse_content(book_idx: int, chap_idx: int, verse_idx: int) -> Tuple[List[str], str]:
    cols, _ = shutil.get_terminal_size(fallback=(80, 24))
    content_width = cols - 4
    
    book_name, chapter_number, verses = get_book_chapter(book_idx, chap_idx)
    
    if 0 <= verse_idx < len(verses):
        v = verses[verse_idx]
        verse_num = v.get("verse", str(verse_idx + 1))
        text = v.get("text", "")
        
        header = f"{book_name} {chapter_number}:{verse_num}"
        
        # Wrap text
        lines = textwrap.wrap(text, width=content_width) or [""]
    else:
        header = f"{book_name} {chapter_number}:?"
        lines = ["Verse not found."]
        
    return lines, header

def display_viewport(lines: List[str], header: str, offset: int) -> int:
    _, rows = shutil.get_terminal_size(fallback=(80, 24))
    
    reserved_outside = 1 # Footer
    box_borders = 2 # Top and Bottom
    fixed_header_lines = 3 # Header, KJV, Blank
    
    total_reserved = reserved_outside + box_borders + fixed_header_lines
    verse_lines_available = max(1, rows - total_reserved)
    
    clear_screen()
    
    visible_lines = lines[offset: offset + verse_lines_available]
    
    # Construct the content for the box
    box_content_lines = [
        header,
        "King James Version",
        ""
    ] + visible_lines
    
    full_text = "\n".join(box_content_lines)
    UI.print_box(full_text)
        
    print("< PREV | NEXT > | [S]earch | [M]enu")
    return verse_lines_available

def menu_select(items: List[str], title: str) -> int:
    if not items: return -1
    idx = 0
    
    while True:
        cols, rows = shutil.get_terminal_size(fallback=(80, 24))
        reserved_lines = 4  # Title (2) + Footer (2)
        available_height = max(1, rows - reserved_lines)
        
        total = len(items)
        items_per_col = available_height
        num_cols = (total + items_per_col - 1) // items_per_col
        
        max_w = max((len(it) for it in items), default=0) + 4
        
        clear_screen()
        print(title + "\n")
        
        for r in range(items_per_col):
            row_parts = []
            for c in range(num_cols):
                i = c * items_per_col + r
                if i < total:
                    name = items[i]
                    disp = f"[{name}]" if i == idx else f" {name} "
                    row_parts.append(disp.ljust(max_w))
            print("".join(row_parts))
            
        print("\n[ENTER] Confirm | [ESC] Back | [Q] Quit Menu")
        
        k = readkey()
        if k == key.UP:
            idx = (idx - 1) % total
        elif k == key.DOWN:
            idx = (idx + 1) % total
        elif k == key.LEFT:
            new_idx = idx - items_per_col
            if new_idx < 0:
                idx = max(0, idx - items_per_col)
            else:
                idx = new_idx
        elif k == key.RIGHT:
            new_idx = idx + items_per_col
            if new_idx >= total:
                idx = min(total - 1, idx + items_per_col)
            else:
                idx = new_idx
        elif k == key.ENTER:
            return idx
        elif k == key.ESC or k in ("q", "Q"):
            return -1

def search_menu() -> Optional[Tuple[int, int, int]]:
    # Select Book
    books = [b.get("book", "") for b in KJV_BIBLE]
    b_idx = menu_select(books, "Select Book:")
    if b_idx == -1: return None
    
    # Select Chapter
    try:
        ch_count = len(KJV_BIBLE[b_idx].get("chapters", []))
    except:
        ch_count = 0
    
    if ch_count <= 1:
        c_idx = 0
    else:
        chapters = [str(i + 1) for i in range(ch_count)]
        c_idx = menu_select(chapters, f"[{books[b_idx]}] - Select Chapter:")
        if c_idx == -1: return None

    # Select Verse
    try:
        v_count = len(KJV_BIBLE[b_idx]["chapters"][c_idx].get("verses", []))
    except:
        v_count = 0
        
    if v_count == 0:
        v_idx = 0
    else:
        verses = [str(i + 1) for i in range(v_count)]
        v_idx = menu_select(verses, f"[{books[b_idx]} {c_idx + 1}] - Select Verse:")
        if v_idx == -1: return None
        
    return b_idx, c_idx, v_idx

def get_nav_target_verse(book_idx: int, chap_idx: int, verse_idx: int, direction: int) -> Tuple[int, int, int]:
    # direction: -1 for prev, 1 for next
    books_len = len(KJV_BIBLE)
    if books_len == 0: return 0, 0, 0
    
    chapters = KJV_BIBLE[book_idx].get("chapters", [])
    verses = chapters[chap_idx].get("verses", [])
    verses_len = len(verses)
    
    new_verse = verse_idx + direction
    
    if 0 <= new_verse < verses_len:
        return book_idx, chap_idx, new_verse
    
    # Move to adjacent chapter
    if direction > 0:
        # Next chapter
        new_chap = chap_idx + 1
        if new_chap < len(chapters):
            return book_idx, new_chap, 0
        else:
            # Next book
            new_book = (book_idx + 1) % books_len
            return new_book, 0, 0
    else:
        # Prev chapter
        new_chap = chap_idx - 1
        if new_chap >= 0:
            prev_verses_len = len(chapters[new_chap].get("verses", []))
            return book_idx, new_chap, max(0, prev_verses_len - 1)
        else:
            # Prev book
            new_book = (book_idx - 1) % books_len
            prev_book_chapters = KJV_BIBLE[new_book].get("chapters", [])
            last_chap_idx = max(0, len(prev_book_chapters) - 1)
            last_chap_verses_len = len(prev_book_chapters[last_chap_idx].get("verses", [])) if prev_book_chapters else 0
            return new_book, last_chap_idx, max(0, last_chap_verses_len - 1)

def start():
    # Initial Search
    res = search_menu()
    if not res: return
    
    cur_book, cur_chap, cur_verse = res
    lines, header = get_verse_content(cur_book, cur_chap, cur_verse)
    offset = 0
    
    while True:
        content_height = display_viewport(lines, header, offset)
        k = readkey()
        
        if k == key.UP:
            offset = max(0, offset - 1)
        elif k == key.DOWN:
            max_offset = max(0, len(lines) - content_height)
            offset = min(max_offset, offset + 1)
        elif k in ("s", "S"):
            res = search_menu()
            if res:
                cur_book, cur_chap, cur_verse = res
                lines, header = get_verse_content(cur_book, cur_chap, cur_verse)
                offset = 0
        elif k == key.LEFT:
            cur_book, cur_chap, cur_verse = get_nav_target_verse(cur_book, cur_chap, cur_verse, -1)
            lines, header = get_verse_content(cur_book, cur_chap, cur_verse)
            offset = 0
        elif k == key.RIGHT:
            cur_book, cur_chap, cur_verse = get_nav_target_verse(cur_book, cur_chap, cur_verse, 1)
            lines, header = get_verse_content(cur_book, cur_chap, cur_verse)
            offset = 0
        elif k == key.ESC or k in ("m", "M"):
            break

if __name__ == "__main__":
    start()
