try:
    from readchar import readkey, key
except ImportError:
    import os
    print("\nwait lang pu...")
    os.system("pip install readchar")
    from readchar import readkey, key

import random
from recommended_verses import verses

options = [
    "[W] START READING",  # 0
    "[B] BOOKMARKS",      # 1
    "[F] FIND IN BIBLE",  # 2
    "[Q] QUIT"            # 3
]

def open_screen(index):
    if index == 0:
        import screen3_read_bible_books
        screen3_read_bible_books.start()
    elif index == 1:
        import screen4_bookmarks
        screen4_bookmarks.start()
    elif index == 2:
        import screen5_find_in_bible
        screen5_find_in_bible.start()
    elif index == 3:
        exit()

def verse_of_the_day():
    import screen3_read_bible_verse
    from bible_data import KJV_BIBLE
    
    print("Verse of the Day")

    random_verse = random.choice(verses)
    screen3_read_bible_verse.print_verse_box(random_verse[0], random_verse[1], random_verse[2])

# =====
# START
# =====

def start():
    selected_option = 0
    while True:
        print("\033[H\033[2J")  # Clear screen
        print("\nBASTA TITLE NATIN\n")
        verse_of_the_day()
        
        i = 0
        for option in options:
            if selected_option == i:
                print(f"\033[93m{option}\033[0m")
            else:
                print(f"{option}")

            i += 1
        
        # navigation hehe

        pressed_key = readkey()

        if pressed_key == key.DOWN:
            selected_option = (selected_option + 1) % len(options)

        elif pressed_key == key.UP:
            selected_option = (selected_option - 1) % len(options)

        elif pressed_key == key.ENTER:
            open_screen(selected_option)
        
        elif pressed_key.lower() == 'w':
            open_screen(0)
        elif pressed_key.lower() == 'b':
            open_screen(1)
        elif pressed_key.lower() == 'f':
            open_screen(2)
        elif pressed_key.lower() == 'q':
            open_screen(3)