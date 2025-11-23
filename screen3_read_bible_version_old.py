from typing import List, Tuple, Optional
import shutil
import textwrap
from readchar import readkey, key

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

def render_verses_to_lines(verses: List[dict], width: int) -> Tuple[List[str], List[int]]:
    lines: List[str] = []
    verse_starts: List[int] = []
    for v in verses:
        verse_no = str(v.get("verse", ""))
        text = v.get("text", "")
        verse_starts.append(len(lines))
        if not text:
            lines.append(f"{verse_no}")
            continue
        available = max(10, width - (len(verse_no) + 1))
        wrapped = textwrap.wrap(text, width=available) or [""]
        lines.append(f"{verse_no} {wrapped[0]}")
        indent = " " * (len(verse_no) + 1)
        for cont in wrapped[1:]:
            lines.append(f"{indent}{cont}")
    return lines, verse_starts

def get_chapter_content(book_idx: int, chap_idx: int) -> Tuple[List[str], List[int], str]:
    cols, _ = shutil.get_terminal_size(fallback=(80, 24))
    book_name, chapter_number, verses = get_book_chapter(book_idx, chap_idx)
    header = f"{book_name} {chapter_number}".upper()
    lines, verse_starts = render_verses_to_lines(verses, cols)
    return lines, verse_starts, header

def display_viewport(lines: List[str], header: str, offset: int) -> int:
    _, rows = shutil.get_terminal_size(fallback=(80, 24))
    reserved = 3 # Header, blank, footer
    content_height = max(1, rows - reserved)
    
    clear_screen()
    print(header)
    print()
    
    visible = lines[offset: offset + content_height]
    for ln in visible:
        print(ln)
    for _ in range(content_height - len(visible)):
        print()
        
    print("\n< PREV | NEXT > | [S]earch | [M]enu")
    return content_height

def menu_select(items: List[str], title: str) -> int:
    if not items: return -1
    idx = 0
    
    while True:
        cols, rows = shutil.get_terminal_size(fallback=(80, 24))
        reserved_lines = 4  # Title (2) + Footer (2)
        available_height = max(1, rows - reserved_lines)
        
        total = len(items)
        # Calculate columns needed to fit all items within available height
        items_per_col = available_height
        num_cols = (total + items_per_col - 1) // items_per_col
        
        # Calculate column width
        max_w = max((len(it) for it in items), default=0) + 4 # [x] + padding
        
        clear_screen()
        print(title + "\n")
        
        for r in range(items_per_col):
            row_parts = []
            for c in range(num_cols):
                i = c * items_per_col + r
                if i < total:
                    name = items[i]
                    disp = f"[{name}]" if i == idx else f" {name} "
                    # Pad to column width
                    row_parts.append(disp.ljust(max_w))
            print("".join(row_parts))
            
        # Fill remaining lines if any (though we calculated to fit)
        # But if total items < available_height, we might have empty lines at bottom
        # which is fine.
        
        print("\n[ENTER] Confirm | [ESC] Back | [Q] Quit Menu")
        
        k = readkey()
        if k == key.UP:
            idx = (idx - 1) % total
        elif k == key.DOWN:
            idx = (idx + 1) % total
        elif k == key.LEFT:
            # Jump to previous column (same row)
            # If we are at the start, wrap to end? Or stop?
            # Let's wrap around for fluid navigation
            new_idx = idx - items_per_col
            if new_idx < 0:
                # Wrap to end, trying to keep relative row
                # This is a bit complex to get perfectly right with uneven columns
                # Simple approach: just subtract
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

def get_nav_target(book_idx: int, chap_idx: int, direction: int) -> Tuple[int, int]:
    # direction: -1 for prev, 1 for next
    books_len = len(KJV_BIBLE)
    if books_len == 0: return 0, 0
    
    chapters_len = len(KJV_BIBLE[book_idx].get("chapters", []))
    
    new_chap = chap_idx + direction
    
    if 0 <= new_chap < chapters_len:
        return book_idx, new_chap
    
    # Move to adjacent book
    new_book = (book_idx + direction) % books_len
    if direction > 0:
        return new_book, 0
    else:
        # Last chapter of previous book
        prev_chaps = len(KJV_BIBLE[new_book].get("chapters", []))
        return new_book, max(0, prev_chaps - 1)

def start():
    # Initial Search
    res = search_menu()
    if not res: return
    
    cur_book, cur_chap, cur_verse = res
    lines, verse_starts, header = get_chapter_content(cur_book, cur_chap)
    offset = verse_starts[cur_verse] if cur_verse < len(verse_starts) else 0
    
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
                lines, verse_starts, header = get_chapter_content(cur_book, cur_chap)
                offset = verse_starts[cur_verse] if cur_verse < len(verse_starts) else 0
        elif k == key.LEFT:
            cur_book, cur_chap = get_nav_target(cur_book, cur_chap, -1)
            lines, verse_starts, header = get_chapter_content(cur_book, cur_chap)
            offset = 0
        elif k == key.RIGHT:
            cur_book, cur_chap = get_nav_target(cur_book, cur_chap, 1)
            lines, verse_starts, header = get_chapter_content(cur_book, cur_chap)
            offset = 0
        elif k == key.ESC or k in ("m", "M"):
            break


