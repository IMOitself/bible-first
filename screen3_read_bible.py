"""Console Bible chapter reader (KJV).

Features:
- Displays chapter header (BOOK CHAPTER) at top and keeps it while scrolling
- Scrolls through all verse lines with UP/DOWN
- LEFT/RIGHT to go previous/next chapter (wrap-around at Bible ends)
- 'm' or ESC to return to main menu

Usage: import or run this module. Calling `run()` returns to the caller when
the user requests the menu.
"""

from typing import List, Tuple
import shutil
import textwrap
from readchar import readkey, key

try:
    from bible_data import KJV_BIBLE
except Exception:
    KJV_BIBLE = []


def clear_screen() -> None:
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


def render_verses_to_lines(verses: List[dict], width: int) -> List[str]:
    """Convert verses into a flattened list of printable lines with wrapping.

    Each verse begins with the verse number on the first line and subsequent
    wrapped lines are indented to align with the verse text.
    """
    # We'll also record the starting line index of each verse so callers can
    # position the display with a specific verse at the top.
    lines: List[str] = []
    verse_starts: List[int] = []
    for v in verses:
        verse_no = str(v.get("verse", ""))
        text = v.get("text", "")
        verse_starts.append(len(lines))
        if not text:
            lines.append(f"{verse_no}")
            continue

        # Allow a small gutter for verse number + a space
        available = max(10, width - (len(verse_no) + 1))
        wrapped = textwrap.wrap(text, width=available) or [""]

        # First line includes verse number
        first = wrapped[0]
        lines.append(f"{verse_no} {first}")

        # Subsequent lines are indented to align under the verse text
        indent = " " * (len(verse_no) + 1)
        for cont in wrapped[1:]:
            lines.append(f"{indent}{cont}")

    return lines, verse_starts


def display_chapter(book_idx: int, chap_idx: int, offset: int) -> Tuple[int, int]:
    """Render the chapter to the terminal starting at `offset`.

    Returns (num_lines, content_height) so callers can compute bounds.
    """
    cols, rows = shutil.get_terminal_size(fallback=(80, 24))

    book_name, chapter_number, verses = get_book_chapter(book_idx, chap_idx)

    header = f"{book_name} {chapter_number}".upper()

    # Reserve lines: header (1), blank (1), bottom hint (1)
    reserved = 3
    content_height = max(1, rows - reserved)

    lines, verse_starts = render_verses_to_lines(verses, cols)

    max_offset = max(0, len(lines) - content_height)
    offset = max(0, min(offset, max_offset))

    clear_screen()

    # Header
    print(header)
    print()

    # Content window
    visible = lines[offset: offset + content_height]
    for ln in visible:
        print(ln)

    # Fill remaining lines so layout stays consistent
    for _ in range(content_height - len(visible)):
        print()

    # Navigation hint
    print("\n← PREV | NEXT → | [S]earch | [M]enu")

    return len(lines), content_height


def get_lines_and_starts(book_idx: int, chap_idx: int):
    """Return flattened lines and verse starting indices for a chapter."""
    cols, rows = shutil.get_terminal_size(fallback=(80, 24))
    _, _, verses = get_book_chapter(book_idx, chap_idx)
    lines, verse_starts = render_verses_to_lines(verses, cols)
    return lines, verse_starts


def _select_item_list(items: List[str], title: str, per_row: int = 10) -> int:
    """Generic selection UI for a list of string `items`.

    Returns the selected index, or -1 if cancelled/quit.
    """
    total = len(items)
    if total == 0:
        return -1

    idx = 0
    maxlen = max((len(it) for it in items), default=0) + 2

    while True:
        clear_screen()
        print(title)
        print()

        for start in range(0, total, per_row):
            row = []
            for i in range(start, min(start + per_row, total)):
                name = items[i]
                if i == idx:
                    disp = f"[{name}]"
                else:
                    disp = name
                row.append(disp.ljust(maxlen + 2))
            print(" ".join(row))

        print()
        print("[ENTER] Confirm | [ESC] Back | [Q] Quit Menu")

        k = readkey()
        if k == key.LEFT:
            idx = max(0, idx - 1)
        elif k == key.RIGHT:
            idx = min(total - 1, idx + 1)
        elif k == key.UP:
            idx = max(0, idx - per_row)
        elif k == key.DOWN:
            idx = min(total - 1, idx + per_row)
        elif k == key.ENTER:
            return idx
        elif k == key.ESC or k in ("q", "Q"):
            return -1


def select_book() -> int:
    books = [b.get("book", "") for b in KJV_BIBLE]
    return _select_item_list(books, "Select Book:")


def select_chapter(book_idx: int) -> int:
    _, _, verses = get_book_chapter(book_idx, 0)
    # Need number of chapters for the book
    try:
        ch_count = len(KJV_BIBLE[book_idx].get("chapters", []))
    except Exception:
        ch_count = 0

    if ch_count <= 1:
        return 0

    chapters = [str(i + 1) for i in range(ch_count)]
    sel = _select_item_list(chapters, f"[{KJV_BIBLE[book_idx].get('book','')}] - Select Chapter (Total: {ch_count}):")
    return sel


def select_verse(book_idx: int, chap_idx: int) -> int:
    try:
        verses = KJV_BIBLE[book_idx]["chapters"][chap_idx].get("verses", [])
    except Exception:
        verses = []

    vcount = len(verses)
    if vcount == 0:
        return 0

    verses_list = [str(i + 1) for i in range(vcount)]
    sel = _select_item_list(verses_list, f"[{KJV_BIBLE[book_idx].get('book','')} {chap_idx + 1}] - Select Verse (Total: {vcount}):")
    return sel


def search_menu() -> Tuple[int, int, int] | None:
    """Orchestrate three-step book→chapter→verse selection.

    Returns (book_idx, chap_idx, verse_idx) or None if cancelled.
    """
    # Book selection
    b = select_book()
    if b == -1:
        return None

    # Chapter selection (skip if only 1 chapter)
    ch = select_chapter(b)
    if ch == -1:
        return None

    # Verse selection
    v = select_verse(b, ch)
    if v == -1:
        return None

    return b, ch, v


def total_chapters_count() -> Tuple[int, int]:
    """Return total books and list of chapter counts per book."""
    books = len(KJV_BIBLE)
    chapters_per_book = [len(b.get("chapters", [])) for b in KJV_BIBLE]
    return books, chapters_per_book


def prev_chapter(book_idx: int, chap_idx: int) -> Tuple[int, int]:
    books, chapters_per_book = total_chapters_count()
    if books == 0:
        return 0, 0

    if chap_idx > 0:
        return book_idx, chap_idx - 1

    # move to last chapter of previous book (wrap-around allowed)
    prev_book = (book_idx - 1) % books
    prev_chap = max(0, chapters_per_book[prev_book] - 1)
    return prev_book, prev_chap


def next_chapter(book_idx: int, chap_idx: int) -> Tuple[int, int]:
    books, chapters_per_book = total_chapters_count()
    if books == 0:
        return 0, 0

    if chap_idx + 1 < chapters_per_book[book_idx]:
        return book_idx, chap_idx + 1

    # move to first chapter of next book (wrap-around allowed)
    next_book = (book_idx + 1) % books
    return next_book, 0


def run() -> None:
    """Main interactive loop for reading chapters. Always starts at Genesis 1.

    Exits (returns) when user presses 'm' or ESC to go back to menu.
    """
    # Start at Genesis 1
    current_book = 0
    current_chapter = 0
    offset = 0

    # If KJV_BIBLE isn't available, show friendly message and return
    if not KJV_BIBLE:
        clear_screen()
        print("KJV Bible data not found. Please ensure `bible_data.py` exports KJV_BIBLE.")
        input("Press Enter to return to menu...")
        return

    # Pre-render lines for current chapter
    cols, rows = shutil.get_terminal_size(fallback=(80, 24))
    lines, content_height = display_chapter(current_book, current_chapter, offset)

    while True:
        k = readkey()

        if k == key.UP:
            offset = max(0, offset - 1)

        elif k == key.DOWN:
            # compute max_offset based on current chapter lines
            max_offset = max(0, lines - content_height)
            offset = min(max_offset, offset + 1)

        elif k in ("s", "S"):
            # Launch search menu
            res = search_menu()
            if res:
                sb, sc, sv = res
                # compute lines and verse starts for target chapter
                all_lines, verse_starts = get_lines_and_starts(sb, sc)
                # place selected verse at top
                try:
                    offset = verse_starts[sv]
                except Exception:
                    offset = 0
                current_book, current_chapter = sb, sc

        elif k == key.LEFT:
            # previous chapter (wrap-around)
            current_book, current_chapter = prev_chapter(current_book, current_chapter)
            offset = 0

        elif k == key.RIGHT:
            current_book, current_chapter = next_chapter(current_book, current_chapter)
            offset = 0

        elif k == key.ESC or k in ("m", "M"):
            # Return to menu
            break

        # Re-render after any handled key
        lines, content_height = display_chapter(current_book, current_chapter, offset)


def main():
    run()


if __name__ == "__main__":
    main()
