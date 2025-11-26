import random
import UI
from recommended_verses import verses

# install readchar once for all files if not installed
try:
    from readchar import readkey, key
except ImportError:
    import os
    print("\nwait lang pu...")
    os.system("pip install readchar")
    from readchar import readkey, key

# global variable to store the verse of the day
verse_of_the_day_verse = None

# list of menu options
options = [
    "[W] START READING",  # 0
    "[B] BOOKMARKS",      # 1
    "[F] FIND IN BIBLE",  # 2
    "[Q] QUIT"            # 3
]

# function to handle menu selection
def open_screen(index):
    # start reading
    if index == 0:
        import screen3_read_bible_books
        screen3_read_bible_books.start()
    # bookmarks
    elif index == 1:
        import screen4_bookmarks
        screen4_bookmarks.start()
    # find in bible
    elif index == 2:
        import screen5_find_in_bible
        screen5_find_in_bible.start()
    # quit
    elif index == 3:
        exit()

# function to display the verse of the day
def verse_of_the_day():
    import screen3_read_bible_verse
    from bible_data import KJV_BIBLE
    
    print("Verse of the Day")

    global verse_of_the_day_verse
    # select a random verse from the list
    random_verse = random.choice(verses)
    # generate the verse box if not already generated
    if verse_of_the_day_verse == None:
        verse_of_the_day_verse = screen3_read_bible_verse.get_verse_box(random_verse[0], random_verse[1], random_verse[2])
    
    # print the verse box
    UI.print_box(verse_of_the_day_verse)

# =====
# START
# =====

# main function to run the menu
def start():
    # track the currently selected option
    selected_option = 0
    # main loop
    while True:
        print("\033[H\033[2J")  # Clear screen
        print("\nBASTA TITLE NATIN\n")
        # display the verse of the day
        verse_of_the_day()
        
        i = 0
        # loop through options to display them
        for option in options:
            # highlight the selected option
            if selected_option == i:
                # print in yellow
                print(f"\033[93m\033[7m{option}\033[0m")
            else:
                print(f"{option}")

            i += 1
        
        # navigation hehe

        # wait for user input
        pressed_key = readkey()

        # move selection down
        if pressed_key == key.DOWN:
            # wrap around to the top
            selected_option = (selected_option + 1) % len(options)

        # move selection up
        elif pressed_key == key.UP:
            # wrap around to the bottom
            selected_option = (selected_option - 1) % len(options)

        # select the current option
        elif pressed_key == key.ENTER:
            open_screen(selected_option)
        
        # shortcut for start reading
        elif pressed_key.lower() == 'w':
            open_screen(0)
        # shortcut for bookmarks
        elif pressed_key.lower() == 'b':
            open_screen(1)
        # shortcut for find in bible
        elif pressed_key.lower() == 'f':
            open_screen(2)
        # shortcut for quit
        elif pressed_key.lower() == 'q':
            open_screen(3)