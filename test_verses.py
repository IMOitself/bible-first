import sys
import os
from io import StringIO
from unittest.mock import MagicMock

# Mock readchar
sys.modules['readchar'] = MagicMock()
from readchar import key
sys.modules['readchar'].key = key

# Mock UI
sys.modules['UI'] = MagicMock()
from UI import print_box

try:
    import screen3_read_bible_chapters_and_verses
except ImportError:
    print("Could not import screen3_read_bible_chapters_and_verses")
    sys.exit(1)

def test_verse_rendering():
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    
    # Mock readkey sequence:
    # 1. ENTER (Select Chapter 1)
    # 2. 'q' (Back to Chapter selection)
    # 3. 'q' (Exit)
    
    # We need to set side_effect on readkey
    screen3_read_bible_chapters_and_verses.readkey = MagicMock(side_effect=[key.ENTER, 'q', 'q'])
    
    # Test with Genesis (Book 0)
    print("--- Test Genesis Verse Selection ---")
    screen3_read_bible_chapters_and_verses.start(0)
    
    sys.stdout = old_stdout
    output = mystdout.getvalue()
    
    # Check if print_box was called with "Genesis 1:_"
    # It should be called multiple times.
    # 1. "Genesis _:_" (Initial)
    # 2. "Genesis 1:_" (After Enter)
    # 3. "Genesis _:_" (After Back)
    
    calls = screen3_read_bible_chapters_and_verses.UI.print_box.call_args_list
    
    # We expect at least one call with "Genesis 1:_"
    found_verse_header = any("Genesis 1:_" in str(call) for call in calls)
    
    if found_verse_header:
        print("PASS: Verse header 'Genesis 1:_' displayed.")
    else:
        print("FAIL: Verse header NOT displayed.")
        print("Calls:", calls)
        
    # Check output for "Verse:" label
    if "Verse:" in output:
        print("PASS: 'Verse:' label found.")
    else:
        print("FAIL: 'Verse:' label NOT found.")

if __name__ == "__main__":
    test_verse_rendering()
