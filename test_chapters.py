import sys
import os
from io import StringIO
from unittest.mock import patch, MagicMock

# Mock readchar to avoid blocking
sys.modules['readchar'] = MagicMock()
from readchar import key
sys.modules['readchar'].key = key

# Mock UI to capture print_box
sys.modules['UI'] = MagicMock()
from UI import print_box

try:
    import screen3_read_bible_chapters_and_verses
except ImportError:
    print("Could not import screen3_read_bible_chapters_and_verses")
    sys.exit(1)

def test_chapter_rendering():
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    
    # Mock readkey to return 'q' immediately
    screen3_read_bible_chapters_and_verses.readkey = MagicMock(return_value='q')
    
    # Test with Genesis (Book 0)
    print("--- Test Genesis ---")
    screen3_read_bible_chapters_and_verses.start(0)
    
    sys.stdout = old_stdout
    output = mystdout.getvalue()
    
    # Check if print_box was called with correct title
    screen3_read_bible_chapters_and_verses.UI.print_box.assert_called_with("Genesis _:_")
    print("PASS: UI.print_box called with 'Genesis _:_'")
    
    # Check if chapters are printed
    if "01" in output and "50" in output:
        print("PASS: Chapters 01 to 50 found in output.")
    else:
        print("FAIL: Chapters not found.")
        # print(output)

if __name__ == "__main__":
    test_chapter_rendering()
